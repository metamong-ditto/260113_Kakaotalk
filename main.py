#!/usr/bin/env python3
"""
카카오톡 PC 오픈채팅방 인원 수 확인 도구

사용법:
    python main.py                    # 대화형 모드
    python main.py "검색어"           # 직접 검색
    python main.py "검색어" -o result.csv  # CSV로 저장
"""

import argparse
import csv
import sys
from datetime import datetime

from kakao_openchat_scraper import search_openchat, print_results, OpenChatRoom


def export_to_csv(rooms: list[OpenChatRoom], filename: str, keyword: str):
    """검색 결과를 CSV 파일로 저장"""
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["순위", "채팅방 이름", "인원 수", "설명"])

        sorted_rooms = sorted(rooms, key=lambda x: x.member_count, reverse=True)
        for i, room in enumerate(sorted_rooms, 1):
            writer.writerow([
                i,
                room.name,
                room.member_count,
                room.description or ""
            ])

    print(f"\n결과가 '{filename}'에 저장되었습니다.")


def interactive_mode():
    """대화형 모드"""
    print("=" * 60)
    print("카카오톡 PC 오픈채팅방 인원 수 확인 도구")
    print("=" * 60)
    print("\n[필수 조건]")
    print("  1. 카카오톡 PC 버전이 실행되어 있어야 합니다")
    print("  2. 카카오톡에 로그인되어 있어야 합니다")
    print("  3. Tesseract OCR이 설치되어 있어야 합니다")
    print("\n종료하려면 'q' 또는 'quit'를 입력하세요.\n")

    while True:
        try:
            keyword = input("검색할 키워드를 입력하세요: ").strip()

            if keyword.lower() in ("q", "quit", "exit"):
                print("프로그램을 종료합니다.")
                break

            if not keyword:
                print("키워드를 입력해주세요.\n")
                continue

            print(f"\n'{keyword}' 검색 중...")
            print("잠시 기다려주세요. 카카오톡 창이 자동으로 조작됩니다.\n")

            rooms = search_openchat(keyword)

            if rooms:
                print_results(rooms, keyword)

                save = input("\nCSV로 저장하시겠습니까? (y/n): ").strip().lower()
                if save == "y":
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"kakao_openchat_{keyword}_{timestamp}.csv"
                    export_to_csv(rooms, filename, keyword)
            else:
                print(f"'{keyword}'에 대한 검색 결과가 없습니다.")
                print("카카오톡 PC가 실행 중인지 확인해주세요.")

            print("\n" + "-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\n\n프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"오류가 발생했습니다: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="카카오톡 PC 오픈채팅방 검색 및 인원 수 확인 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
    python main.py                        # 대화형 모드
    python main.py "파이썬"               # '파이썬' 검색
    python main.py "영어" -o english.csv  # CSV로 저장

필수 조건:
    - 카카오톡 PC 버전 실행 및 로그인
    - Tesseract OCR 설치 (https://github.com/tesseract-ocr/tesseract)
        """
    )
    parser.add_argument(
        "keyword",
        nargs="?",
        help="검색할 키워드 (없으면 대화형 모드)"
    )
    parser.add_argument(
        "-o", "--output",
        help="결과를 저장할 CSV 파일명"
    )

    args = parser.parse_args()

    if not args.keyword:
        interactive_mode()
        return

    print(f"'{args.keyword}' 키워드로 오픈채팅방 검색 중...")
    print("카카오톡 PC가 실행되어 있어야 합니다.")
    print()

    rooms = search_openchat(args.keyword)

    print_results(rooms, args.keyword)

    if args.output and rooms:
        export_to_csv(rooms, args.output, args.keyword)


if __name__ == "__main__":
    main()
