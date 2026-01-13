#!/usr/bin/env python3
"""
카카오톡 오픈채팅방 인원 수 확인 도구

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
        writer.writerow(["순위", "채팅방 이름", "인원 수", "설명", "링크"])

        sorted_rooms = sorted(rooms, key=lambda x: x.member_count, reverse=True)
        for i, room in enumerate(sorted_rooms, 1):
            writer.writerow([
                i,
                room.name,
                room.member_count,
                room.description or "",
                room.link or ""
            ])

    print(f"\n결과가 '{filename}'에 저장되었습니다.")


def interactive_mode():
    """대화형 모드"""
    print("=" * 60)
    print("카카오톡 오픈채팅방 인원 수 확인 도구")
    print("=" * 60)
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

            max_results_input = input("최대 결과 수 (기본값: 20): ").strip()
            max_results = int(max_results_input) if max_results_input else 20

            print(f"\n'{keyword}' 검색 중...")
            rooms = search_openchat(keyword, max_results)

            if rooms:
                print_results(rooms, keyword)

                save = input("\nCSV로 저장하시겠습니까? (y/n): ").strip().lower()
                if save == "y":
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"kakao_openchat_{keyword}_{timestamp}.csv"
                    export_to_csv(rooms, filename, keyword)
            else:
                print(f"'{keyword}'에 대한 검색 결과가 없습니다.")

            print("\n" + "-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\n\n프로그램을 종료합니다.")
            break
        except ValueError:
            print("올바른 숫자를 입력해주세요.\n")
        except Exception as e:
            print(f"오류가 발생했습니다: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="카카오톡 오픈채팅방 검색 및 인원 수 확인 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
    python main.py                        # 대화형 모드
    python main.py "파이썬"               # '파이썬' 검색
    python main.py "주식" -n 50           # '주식' 검색, 최대 50개
    python main.py "영어" -o english.csv  # CSV로 저장
    python main.py "게임" --no-headless   # 브라우저 표시
        """
    )
    parser.add_argument(
        "keyword",
        nargs="?",
        help="검색할 키워드 (없으면 대화형 모드)"
    )
    parser.add_argument(
        "-n", "--max-results",
        type=int,
        default=20,
        help="최대 결과 수 (기본값: 20)"
    )
    parser.add_argument(
        "-o", "--output",
        help="결과를 저장할 CSV 파일명"
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="브라우저 창을 표시합니다"
    )

    args = parser.parse_args()

    if not args.keyword:
        interactive_mode()
        return

    print(f"'{args.keyword}' 키워드로 오픈채팅방 검색 중...")

    rooms = search_openchat(
        keyword=args.keyword,
        max_results=args.max_results,
        headless=not args.no_headless
    )

    print_results(rooms, args.keyword)

    if args.output and rooms:
        export_to_csv(rooms, args.output, args.keyword)


if __name__ == "__main__":
    main()
