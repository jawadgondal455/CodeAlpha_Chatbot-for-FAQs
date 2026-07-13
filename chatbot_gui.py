"""
chatbot_gui.py
Simple Tkinter chat interface for the FAQ chatbot.
"""

import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

from matcher import FAQMatcher

BG_MAIN = "#0f172a"
BG_CHAT = "#1e293b"
BG_ENTRY = "#334155"
FG_TEXT = "#e2e8f0"
ACCENT = "#38bdf8"
USER_BUBBLE = "#2563eb"
BOT_BUBBLE = "#334155"


class FAQChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FAQ Chatbot")
        self.root.geometry("480x600")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        self.matcher = FAQMatcher("faqs.json")

        self._build_ui()
        self._display_bot_message(
            "Hi! I'm your FAQ assistant. Ask me anything about admissions, fees, or academics."
        )

    def _build_ui(self):
        header = tk.Frame(self.root, bg=ACCENT, height=50)
        header.pack(fill="x", side="top")
        tk.Label(
            header, text="💬 FAQ Chatbot", bg=ACCENT, fg="#0f172a",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        self.chat_area = scrolledtext.ScrolledText(
            self.root, wrap="word", bg=BG_CHAT, fg=FG_TEXT,
            font=("Segoe UI", 10), state="disabled", bd=0,
            padx=10, pady=10
        )
        self.chat_area.pack(fill="both", expand=True, padx=8, pady=8)

        input_frame = tk.Frame(self.root, bg=BG_MAIN)
        input_frame.pack(fill="x", padx=8, pady=(0, 10))

        self.entry = tk.Entry(
            input_frame, bg=BG_ENTRY, fg=FG_TEXT, font=("Segoe UI", 11),
            insertbackground=FG_TEXT, relief="flat"
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        self.entry.bind("<Return>", lambda event: self._handle_send())

        send_btn = tk.Button(
            input_frame, text="Send", bg=ACCENT, fg="#0f172a",
            font=("Segoe UI", 10, "bold"), relief="flat",
            command=self._handle_send, cursor="hand2"
        )
        send_btn.pack(side="right", ipadx=10, ipady=6)

    def _handle_send(self):
        query = self.entry.get().strip()
        if not query:
            return
        self.entry.delete(0, tk.END)
        self._display_user_message(query)
        answer = self.matcher.get_best_answer(query)
        self._display_bot_message(answer)

    def _display_user_message(self, text):
        self._append_message(text, align="right", bubble_color=USER_BUBBLE)

    def _display_bot_message(self, text):
        self._append_message(text, align="left", bubble_color=BOT_BUBBLE)

    def _append_message(self, text, align, bubble_color):
        self.chat_area.configure(state="normal")
        timestamp = datetime.now().strftime("%H:%M")
        tag_name = f"tag_{self.chat_area.index('end')}"

        prefix = "You" if align == "right" else "Bot"
        line = f"{prefix} ({timestamp}): {text}\n\n"

        self.chat_area.insert(tk.END, line, tag_name)
        self.chat_area.tag_configure(
            tag_name, foreground=FG_TEXT,
            justify="right" if align == "right" else "left"
        )
        self.chat_area.configure(state="disabled")
        self.chat_area.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = FAQChatbotApp(root)
    root.mainloop()