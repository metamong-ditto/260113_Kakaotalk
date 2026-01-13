#!/usr/bin/env python3
"""
카카오톡 오픈채팅방 인원 수 확인 도구 - GUI 버전
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import csv
from datetime import datetime

from kakao_openchat_scraper import KakaoTalkPCAutomation, OpenChatRoom


class KakaoOpenChatGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("카카오톡 오픈채팅 인원 확인")
        self.root.geometry("700x550")
        self.root.minsize(600, 450)

        # 결과 저장용
        self.rooms = []
        self.automation = KakaoTalkPCAutomation()

        self.setup_ui()

    def setup_ui(self):
        """UI 구성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # === 안내 메시지 ===
        info_frame = ttk.LabelFrame(main_frame, text="사용 방법", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))

        info_text = "1. 카카오톡 PC에서 오픈채팅 검색 화면을 열어주세요\n2. 검색창에 커서를 클릭해주세요\n3. 아래에 검색어를 입력하고 [검색] 버튼을 클릭하세요"
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)

        # === 검색 영역 ===
        search_frame = ttk.LabelFrame(main_frame, text="검색", padding="10")
        search_frame.pack(fill=tk.X, pady=(0, 10))

        # 검색어 입력
        ttk.Label(search_frame, text="검색어:").pack(side=tk.LEFT)

        self.keyword_var = tk.StringVar()
        self.keyword_entry = ttk.Entry(search_frame, textvariable=self.keyword_var, width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=(5, 10))
        self.keyword_entry.bind('<Return>', lambda e: self.start_search())

        # 검색 버튼
        self.search_btn = ttk.Button(search_frame, text="검색", command=self.start_search)
        self.search_btn.pack(side=tk.LEFT, padx=(0, 5))

        # CSV 저장 버튼
        self.save_btn = ttk.Button(search_frame, text="CSV 저장", command=self.save_csv, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT)

        # === 결과 테이블 ===
        result_frame = ttk.LabelFrame(main_frame, text="검색 결과", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 트리뷰 (테이블)
        columns = ("rank", "name", "members")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=10)

        self.tree.heading("rank", text="순위")
        self.tree.heading("name", text="채팅방 이름")
        self.tree.heading("members", text="인원 수")

        self.tree.column("rank", width=50, anchor=tk.CENTER)
        self.tree.column("name", width=400)
        self.tree.column("members", width=100, anchor=tk.CENTER)

        # 스크롤바
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # === 하단: 상태 및 통계 ===
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X)

        # 상태 표시
        self.status_var = tk.StringVar(value="카카오톡 오픈채팅 검색 화면을 준비해주세요.")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT)

        # 통계 표시
        self.stats_var = tk.StringVar(value="")
        self.stats_label = ttk.Label(status_frame, textvariable=self.stats_var)
        self.stats_label.pack(side=tk.RIGHT)

        # 프로그레스바
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(5, 0))

        # 크레딧
        credit_label = ttk.Label(main_frame, text="By. 소도몰 이예하 과장", font=("", 8), foreground="gray")
        credit_label.pack(side=tk.RIGHT, pady=(5, 0))

    def start_search(self):
        """검색 시작"""
        keyword = self.keyword_var.get().strip()

        if not keyword:
            messagebox.showwarning("경고", "검색어를 입력하세요.")
            return

        # 사용자 확인
        if not messagebox.askokcancel(
            "검색 시작",
            "카카오톡 오픈채팅 검색창에 커서가 있나요?\n\n"
            "[확인]을 누르면 3초 후 자동으로 검색어가 입력됩니다.\n"
            "3초 안에 카카오톡 검색창을 클릭해주세요!"
        ):
            return

        # UI 상태 변경
        self.search_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.status_var.set("3초 후 검색을 시작합니다... 카카오톡 검색창을 클릭하세요!")
        self.progress.start()

        # 결과 초기화
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.rooms = []
        self.stats_var.set("")

        # 3초 후 검색 시작
        self.root.after(3000, lambda: self.delayed_search(keyword))

    def delayed_search(self, keyword: str):
        """3초 후 실제 검색 시작"""
        self.status_var.set(f"'{keyword}' 검색 중...")

        # 별도 스레드에서 검색 실행
        thread = threading.Thread(target=self.do_search, args=(keyword,))
        thread.daemon = True
        thread.start()

    def do_search(self, keyword: str):
        """실제 검색 수행 (별도 스레드)"""
        try:
            rooms = self.automation.search_and_get_results(keyword)
            self.root.after(0, lambda: self.show_results(rooms, keyword))
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))

    def show_results(self, rooms: list[OpenChatRoom], keyword: str):
        """검색 결과 표시"""
        self.progress.stop()
        self.search_btn.config(state=tk.NORMAL)

        self.rooms = rooms

        if not rooms:
            self.status_var.set(f"'{keyword}' 검색 결과가 없습니다. (OCR 인식 실패일 수 있음)")
            return

        # 인원 수 기준 정렬
        sorted_rooms = sorted(rooms, key=lambda x: x.member_count, reverse=True)

        # 테이블에 추가
        for i, room in enumerate(sorted_rooms, 1):
            self.tree.insert("", tk.END, values=(i, room.name, f"{room.member_count:,}명"))

        # 통계 계산
        total = sum(r.member_count for r in rooms)
        avg = total / len(rooms)
        max_m = max(r.member_count for r in rooms)
        min_m = min(r.member_count for r in rooms)

        self.status_var.set(f"'{keyword}' 검색 완료: {len(rooms)}개 채팅방")
        self.stats_var.set(f"총: {total:,}명 | 평균: {avg:,.0f}명 | 최대: {max_m:,}명 | 최소: {min_m:,}명")
        self.save_btn.config(state=tk.NORMAL)

    def show_error(self, error: str):
        """에러 표시"""
        self.progress.stop()
        self.search_btn.config(state=tk.NORMAL)
        self.status_var.set(f"오류: {error}")
        messagebox.showerror("오류", error)

    def save_csv(self):
        """CSV 파일로 저장"""
        if not self.rooms:
            messagebox.showwarning("경고", "저장할 결과가 없습니다.")
            return

        keyword = self.keyword_var.get().strip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"kakao_openchat_{keyword}_{timestamp}.csv"

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV 파일", "*.csv"), ("모든 파일", "*.*")],
            initialfile=default_name
        )

        if not filepath:
            return

        try:
            with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["순위", "채팅방 이름", "인원 수"])

                sorted_rooms = sorted(self.rooms, key=lambda x: x.member_count, reverse=True)
                for i, room in enumerate(sorted_rooms, 1):
                    writer.writerow([i, room.name, room.member_count])

            messagebox.showinfo("저장 완료", f"파일이 저장되었습니다:\n{filepath}")
        except Exception as e:
            messagebox.showerror("저장 실패", f"파일 저장 중 오류가 발생했습니다:\n{e}")

    def run(self):
        """앱 실행"""
        self.root.mainloop()


def main():
    app = KakaoOpenChatGUI()
    app.run()


if __name__ == "__main__":
    main()
