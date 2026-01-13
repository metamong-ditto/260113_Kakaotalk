"""
카카오톡 PC 오픈채팅 검색 자동화

카카오톡 PC 버전에서 오픈채팅을 검색하고 채팅방 인원 수를 확인합니다.
PyAutoGUI와 pywinauto를 사용한 GUI 자동화 방식입니다.
"""

import time
import re
from dataclasses import dataclass
from typing import Optional
import subprocess
import os

try:
    import pyautogui
    import pyperclip
    from PIL import Image
    import pytesseract
except ImportError as e:
    print(f"필요한 라이브러리가 없습니다: {e}")
    print("설치: pip install pyautogui pyperclip pillow pytesseract")
    raise

try:
    import pywinauto
    from pywinauto import Application
    PYWINAUTO_AVAILABLE = True
except ImportError:
    PYWINAUTO_AVAILABLE = False


@dataclass
class OpenChatRoom:
    """오픈채팅방 정보를 담는 데이터 클래스"""
    name: str
    member_count: int
    description: Optional[str] = None


class KakaoTalkPCAutomation:
    """카카오톡 PC 자동화 클래스"""

    KAKAO_PROCESS_NAME = "KakaoTalk.exe"

    def __init__(self):
        self.app = None
        self.main_window = None

        # PyAutoGUI 설정
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5

    def find_kakao_window(self) -> bool:
        """카카오톡 창 찾기"""
        if PYWINAUTO_AVAILABLE:
            try:
                self.app = Application(backend="uia").connect(path=self.KAKAO_PROCESS_NAME)
                windows = self.app.windows()
                for win in windows:
                    if "카카오톡" in win.window_text():
                        self.main_window = win
                        return True
            except Exception:
                pass

        # pywinauto 실패 시 pyautogui로 시도
        windows = pyautogui.getWindowsWithTitle("카카오톡")
        if windows:
            windows[0].activate()
            time.sleep(0.5)
            return True

        return False

    def is_kakao_running(self) -> bool:
        """카카오톡 실행 여부 확인"""
        try:
            result = subprocess.run(
                ['tasklist', '/FI', f'IMAGENAME eq {self.KAKAO_PROCESS_NAME}'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return self.KAKAO_PROCESS_NAME.lower() in result.stdout.lower()
        except Exception:
            return False

    def activate_window(self):
        """카카오톡 창 활성화"""
        if self.main_window and PYWINAUTO_AVAILABLE:
            try:
                self.main_window.set_focus()
                return
            except Exception:
                pass

        windows = pyautogui.getWindowsWithTitle("카카오톡")
        if windows:
            windows[0].activate()
            time.sleep(0.3)

    def click_openchat_tab(self):
        """오픈채팅 탭 클릭"""
        self.activate_window()
        time.sleep(0.3)

        # 오픈채팅 아이콘 위치 찾기 (화면에서 이미지 검색)
        # 일반적으로 카카오톡 하단에 있는 말풍선 모양 아이콘
        try:
            # '#' 모양 아이콘 또는 오픈채팅 탭 클릭
            # 카카오톡 창 기준 상대 좌표 사용
            windows = pyautogui.getWindowsWithTitle("카카오톡")
            if windows:
                win = windows[0]
                # 오픈채팅 탭은 보통 왼쪽 사이드바에 있음
                # 대략적인 위치: 창 왼쪽에서 약 30px, 상단에서 약 200px
                x = win.left + 30
                y = win.top + 200
                pyautogui.click(x, y)
                time.sleep(0.5)
        except Exception as e:
            print(f"오픈채팅 탭 클릭 실패: {e}")

    def search_openchat(self, keyword: str):
        """오픈채팅 검색"""
        self.activate_window()
        time.sleep(0.3)

        # Ctrl+F로 검색창 열기 또는 검색 영역 클릭
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)

        # 기존 텍스트 지우기
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)

        # 검색어 입력 (클립보드 사용으로 한글 입력 문제 해결)
        pyperclip.copy(keyword)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)

        # 엔터로 검색
        pyautogui.press('enter')
        time.sleep(1)

    def capture_search_results(self) -> Optional[Image.Image]:
        """검색 결과 영역 캡처"""
        windows = pyautogui.getWindowsWithTitle("카카오톡")
        if not windows:
            return None

        win = windows[0]

        # 검색 결과 영역 캡처 (대략적인 영역)
        left = win.left + 60
        top = win.top + 150
        width = win.width - 80
        height = win.height - 200

        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        return screenshot

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

            # 인원 수 패턴 찾기 (예: "1,234명", "999+명", "123")
            member_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)\s*(?:명|\+)', line)

            if member_match:
                member_count = int(member_match.group(1).replace(',', ''))
                if current_name:
                    rooms.append(OpenChatRoom(
                        name=current_name,
                        member_count=member_count
                    ))
                    current_name = None
            elif len(line) > 2 and not line.isdigit():
                # 채팅방 이름으로 추정
                current_name = line

        return rooms

    def search_and_get_results(self, keyword: str) -> list[OpenChatRoom]:
        """검색 실행 및 결과 반환"""
        if not self.is_kakao_running():
            print("카카오톡이 실행되어 있지 않습니다.")
            print("카카오톡 PC를 먼저 실행해주세요.")
            return []

        if not self.find_kakao_window():
            print("카카오톡 창을 찾을 수 없습니다.")
            return []

        # 오픈채팅 탭으로 이동
        self.click_openchat_tab()
        time.sleep(0.5)

        # 검색 실행
        self.search_openchat(keyword)
        time.sleep(1)

        # 결과 캡처
        image = self.capture_search_results()
        if not image:
            print("검색 결과 캡처 실패")
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
    print("카카오톡 PC가 실행되어 있어야 합니다.")
    print()

    rooms = search_openchat(args.keyword)
    print_results(rooms, args.keyword)
