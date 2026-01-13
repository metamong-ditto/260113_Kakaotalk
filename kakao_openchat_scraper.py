"""
카카오톡 PC 오픈채팅 검색 자동화

사용자가 오픈채팅 검색 화면까지 이동한 후,
검색어 입력과 결과 인식을 자동화합니다.
"""

import time
import re
from dataclasses import dataclass
from typing import Optional

try:
    import pyautogui
    import pyperclip
    from PIL import Image
    import pytesseract
except ImportError as e:
    print(f"필요한 라이브러리가 없습니다: {e}")
    print("설치: pip install pyautogui pyperclip pillow pytesseract")
    raise


@dataclass
class OpenChatRoom:
    """오픈채팅방 정보를 담는 데이터 클래스"""
    name: str
    member_count: int
    description: Optional[str] = None


class KakaoTalkPCAutomation:
    """카카오톡 PC 자동화 클래스"""

    def __init__(self):
        # PyAutoGUI 설정
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.3

    def input_search_keyword(self, keyword: str):
        """
        검색어 입력 (사용자가 이미 검색창에 포커스를 맞춘 상태)
        """
        # 기존 텍스트 지우기
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)

        # 검색어 입력 (클립보드 사용으로 한글 입력 문제 해결)
        pyperclip.copy(keyword)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)

        # 엔터로 검색
        pyautogui.press('enter')
        time.sleep(1.5)  # 검색 결과 로딩 대기

    def capture_screen(self) -> Image.Image:
        """현재 화면 캡처"""
        screenshot = pyautogui.screenshot()
        return screenshot

    def capture_active_window(self) -> Optional[Image.Image]:
        """활성 창 캡처"""
        try:
            windows = pyautogui.getWindowsWithTitle("카카오톡")
            if windows:
                win = windows[0]
                # 창 영역만 캡처
                screenshot = pyautogui.screenshot(region=(
                    win.left, win.top, win.width, win.height
                ))
                return screenshot
        except:
            pass

        # 실패시 전체 화면 캡처
        return pyautogui.screenshot()

    def extract_text_from_image(self, image: Image.Image) -> str:
        """이미지에서 텍스트 추출 (OCR)"""
        try:
            # Tesseract OCR 사용 (한글 지원)
            text = pytesseract.image_to_string(image, lang='kor+eng')
            return text
        except Exception as e:
            print(f"OCR 실패: {e}")
            print("Tesseract가 설치되어 있는지 확인하세요.")
            return ""

    def parse_search_results(self, text: str) -> list[OpenChatRoom]:
        """OCR 텍스트에서 채팅방 정보 파싱"""
        rooms = []
        lines = text.strip().split('\n')

        current_name = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 인원 수 패턴 찾기 (예: "1,234명", "999+명", "123명", "1234")
            member_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)\s*(?:명|\+|$)', line)

            if member_match:
                member_text = member_match.group(1).replace(',', '')
                member_count = int(member_text)

                # 너무 작은 숫자는 무시 (날짜 등일 수 있음)
                if member_count >= 10 and current_name:
                    rooms.append(OpenChatRoom(
                        name=current_name,
                        member_count=member_count
                    ))
                    current_name = None
            elif len(line) > 2 and not line.isdigit():
                # 채팅방 이름으로 추정
                # 특수 문자나 너무 짧은 것 제외
                if not re.match(r'^[\d\s\.\-\:\,]+$', line):
                    current_name = line

        return rooms

    def search_and_get_results(self, keyword: str) -> list[OpenChatRoom]:
        """검색 실행 및 결과 반환"""
        # 검색어 입력
        self.input_search_keyword(keyword)

        # 잠시 대기 후 캡처
        time.sleep(1)

        # 결과 캡처
        image = self.capture_active_window()
        if not image:
            print("화면 캡처 실패")
            return []

        # OCR로 텍스트 추출
        text = self.extract_text_from_image(image)

        # 결과 파싱
        rooms = self.parse_search_results(text)

        return rooms


def search_openchat(keyword: str) -> list[OpenChatRoom]:
    """
    카카오톡 PC에서 오픈채팅 검색

    Args:
        keyword: 검색할 키워드

    Returns:
        검색된 오픈채팅방 목록
    """
    automation = KakaoTalkPCAutomation()
    return automation.search_and_get_results(keyword)


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
            print(f"   설명: {room.description}")
        print()

    # 통계 정보
    if rooms:
        total_members = sum(room.member_count for room in rooms)
        avg_members = total_members / len(rooms)

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
        description="카카오톡 PC 오픈채팅 검색 및 인원 수 확인"
    )
    parser.add_argument(
        "keyword",
        help="검색할 키워드"
    )

    args = parser.parse_args()

    print(f"'{args.keyword}' 키워드로 오픈채팅 검색 중...")
    print("카카오톡 오픈채팅 검색 화면에 포커스를 맞춰주세요!")
    print()

    rooms = search_openchat(args.keyword)
    print_results(rooms, args.keyword)
