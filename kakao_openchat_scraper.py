"""
카카오톡 오픈채팅방 검색 및 인원 수 확인 프로그램

특정 키워드로 오픈채팅방을 검색하고, 채팅방 이름과 인원 수를 출력합니다.
"""

import time
import re
from dataclasses import dataclass
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class OpenChatRoom:
    """오픈채팅방 정보를 담는 데이터 클래스"""
    name: str
    member_count: int
    description: Optional[str] = None
    link: Optional[str] = None


class KakaoOpenChatScraper:
    """카카오 오픈채팅 검색 스크래퍼"""

    SEARCH_URL = "https://open.kakao.com/o/search"

    def __init__(self, headless: bool = True):
        """
        스크래퍼 초기화

        Args:
            headless: 브라우저를 헤드리스 모드로 실행할지 여부
        """
        self.headless = headless
        self.driver = None

    def _setup_driver(self) -> webdriver.Chrome:
        """Chrome 드라이버 설정"""
        options = Options()

        if self.headless:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _parse_member_count(self, text: str) -> int:
        """
        인원 수 텍스트를 숫자로 변환

        예: "1,234명" -> 1234, "999+" -> 999
        """
        text = text.replace(",", "").replace("명", "").replace("+", "").strip()
        match = re.search(r"\d+", text)
        return int(match.group()) if match else 0

    def search(self, keyword: str, max_results: int = 20) -> list[OpenChatRoom]:
        """
        키워드로 오픈채팅방 검색

        Args:
            keyword: 검색할 키워드
            max_results: 최대 결과 수

        Returns:
            검색된 오픈채팅방 목록
        """
        results = []

        try:
            self.driver = self._setup_driver()
            search_url = f"{self.SEARCH_URL}?q={keyword}"
            self.driver.get(search_url)

            # 페이지 로딩 대기
            time.sleep(3)

            # 검색 결과가 로드될 때까지 대기
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.list_search"))
                )
            except TimeoutException:
                print(f"검색 결과를 찾을 수 없습니다: '{keyword}'")
                return results

            # 스크롤하여 더 많은 결과 로드
            self._scroll_to_load_more(max_results)

            # 검색 결과 파싱
            chat_items = self.driver.find_elements(
                By.CSS_SELECTOR, "ul.list_search > li"
            )

            for item in chat_items[:max_results]:
                try:
                    room = self._parse_chat_item(item)
                    if room:
                        results.append(room)
                except Exception as e:
                    print(f"항목 파싱 중 오류: {e}")
                    continue

        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None

        return results

    def _scroll_to_load_more(self, target_count: int):
        """스크롤하여 더 많은 결과 로드"""
        last_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 10

        while scroll_attempts < max_scroll_attempts:
            items = self.driver.find_elements(
                By.CSS_SELECTOR, "ul.list_search > li"
            )
            current_count = len(items)

            if current_count >= target_count or current_count == last_count:
                break

            last_count = current_count
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(1)
            scroll_attempts += 1

    def _parse_chat_item(self, item) -> Optional[OpenChatRoom]:
        """채팅방 항목 파싱"""
        try:
            # 채팅방 이름
            name_elem = item.find_element(By.CSS_SELECTOR, "strong.tit_name")
            name = name_elem.text.strip()

            # 인원 수
            try:
                member_elem = item.find_element(By.CSS_SELECTOR, "span.txt_member")
                member_text = member_elem.text
                member_count = self._parse_member_count(member_text)
            except NoSuchElementException:
                # 인원 수가 표시되지 않는 경우 (1:1 채팅방 등)
                member_count = 0

            # 설명
            try:
                desc_elem = item.find_element(By.CSS_SELECTOR, "p.desc")
                description = desc_elem.text.strip()
            except NoSuchElementException:
                description = None

            # 링크
            try:
                link_elem = item.find_element(By.CSS_SELECTOR, "a")
                link = link_elem.get_attribute("href")
            except NoSuchElementException:
                link = None

            return OpenChatRoom(
                name=name,
                member_count=member_count,
                description=description,
                link=link
            )

        except NoSuchElementException:
            return None


def search_openchat(keyword: str, max_results: int = 20, headless: bool = True) -> list[OpenChatRoom]:
    """
    카카오 오픈채팅방 검색 함수

    Args:
        keyword: 검색할 키워드
        max_results: 최대 결과 수
        headless: 헤드리스 모드 사용 여부

    Returns:
        검색된 오픈채팅방 목록
    """
    scraper = KakaoOpenChatScraper(headless=headless)
    return scraper.search(keyword, max_results)


def print_results(rooms: list[OpenChatRoom], keyword: str):
    """검색 결과 출력"""
    print(f"\n{'='*60}")
    print(f"'{keyword}' 검색 결과: 총 {len(rooms)}개 채팅방")
    print(f"{'='*60}\n")

    if not rooms:
        print("검색 결과가 없습니다.")
        return

    # 인원 수 기준 내림차순 정렬
    sorted_rooms = sorted(rooms, key=lambda x: x.member_count, reverse=True)

    for i, room in enumerate(sorted_rooms, 1):
        print(f"{i}. {room.name}")
        print(f"   인원: {room.member_count:,}명")
        if room.description:
            # 설명이 너무 길면 자르기
            desc = room.description[:50] + "..." if len(room.description) > 50 else room.description
            print(f"   설명: {desc}")
        if room.link:
            print(f"   링크: {room.link}")
        print()

    # 통계 정보
    total_members = sum(room.member_count for room in rooms)
    avg_members = total_members / len(rooms) if rooms else 0

    print(f"{'='*60}")
    print(f"통계:")
    print(f"  - 총 채팅방 수: {len(rooms)}개")
    print(f"  - 총 인원 수: {total_members:,}명")
    print(f"  - 평균 인원 수: {avg_members:,.1f}명")
    print(f"  - 최대 인원: {max(room.member_count for room in rooms):,}명")
    print(f"  - 최소 인원: {min(room.member_count for room in rooms):,}명")
    print(f"{'='*60}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="카카오톡 오픈채팅방 검색 및 인원 수 확인"
    )
    parser.add_argument(
        "keyword",
        help="검색할 키워드"
    )
    parser.add_argument(
        "-n", "--max-results",
        type=int,
        default=20,
        help="최대 결과 수 (기본값: 20)"
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="브라우저 창을 표시합니다"
    )

    args = parser.parse_args()

    print(f"'{args.keyword}' 키워드로 오픈채팅방 검색 중...")

    rooms = search_openchat(
        keyword=args.keyword,
        max_results=args.max_results,
        headless=not args.no_headless
    )

    print_results(rooms, args.keyword)
