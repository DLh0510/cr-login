"""赛博朋克风格登录窗口"""
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import threading
import random
import os
import sys

from ..config import CONFIG
from ..services.login_service import LoginService


def resource_path(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    return os.path.join(base, path)


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.login_service = LoginService(CONFIG["url"])
        self._setup_window()
        self._create_ui()
        self._start_log_animation()
    
    def _setup_window(self):
        self.title(f"{CONFIG['title']}")
        self.geometry("480x650")
        self.resizable(False, False)
        self.configure(fg_color="#0f0a1e")
        ctk.set_appearance_mode("dark")
    
    def _create_ui(self):
        main = ctk.CTkFrame(self, fg_color="#0f0a1e", border_width=2, border_color="#7c3aed", corner_radius=12)
        main.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkFrame(main, height=3, fg_color="#a78bfa").pack(fill="x", pady=(10,0))
        
        content = ctk.CTkFrame(main, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=25, pady=20)
        
        self._create_header(content)
        self._create_form(content)
        self._create_log_panel(content)
        self._create_footer(content)
    
    def _create_header(self, parent):
        try:
            img = ctk.CTkImage(Image.open(resource_path(CONFIG["logo_file"])), size=(80, 80))
            ctk.CTkLabel(parent, image=img, text="").pack(pady=(5, 10))
        except:
            ctk.CTkLabel(parent, text="🤖", font=ctk.CTkFont(size=50)).pack(pady=(5, 10))

        ctk.CTkLabel(parent, text=CONFIG["title"], font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#a78bfa").pack(pady=(5, 2))
        ctk.CTkLabel(parent, text=CONFIG["subtitle"], font=ctk.CTkFont(size=12),
                     text_color="#7c3aed").pack(pady=(2, 15))
    
    def _create_form(self, parent):
        form = ctk.CTkFrame(parent, fg_color="transparent")
        form.pack(fill="x", pady=5)
        
        self.user_entry = self._create_input(form, "学员账号 / Student Account", "user")
        self.pass_entry = self._create_input(form, "登录密码 / Password", "pass", show="●")
        
        opt_frame = ctk.CTkFrame(form, fg_color="transparent")
        opt_frame.pack(fill="x", pady=(5, 15))
        ctk.CTkCheckBox(opt_frame, text="记住账号", font=ctk.CTkFont(size=11),
                        text_color="#a78bfa", fg_color="#7c3aed", border_color="#5b21b6").pack(side="left")
        ctk.CTkLabel(opt_frame, text="忘记密码？", font=ctk.CTkFont(size=11), text_color="#a78bfa", cursor="hand2").pack(side="right")

        self.login_btn = ctk.CTkButton(form, text="🚀  进入课程平台 / LOGIN", height=50, corner_radius=8,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       fg_color="#7c3aed", hover_color="#6d28d9", text_color="#ffffff",
                                       command=self._handle_login)
        self.login_btn.pack(fill="x", pady=(5, 0))
        self.pass_entry.bind('<Return>', lambda e: self._handle_login())
    
    def _create_input(self, parent, placeholder, name, show=None):
        frame = ctk.CTkFrame(parent, fg_color="#1a1232", border_width=1, border_color="#5b21b6", corner_radius=8)
        frame.pack(fill="x", pady=(0, 12))

        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=10)

        entry = ctk.CTkEntry(inner, placeholder_text=placeholder, border_width=0, fg_color="transparent",
                            text_color="#f3f0ff", placeholder_text_color="#6b4fc3", font=ctk.CTkFont(size=13),
                            height=30, show=show)
        entry.pack(side="left", fill="x", expand=True)

        icon = "👤" if name == "user" else "🔑"
        ctk.CTkLabel(inner, text=icon, font=ctk.CTkFont(size=16), text_color="#7c3aed").pack(side="right")
        return entry
    
    def _create_log_panel(self, parent):
        ctk.CTkFrame(parent, height=2, fg_color="#5b21b6").pack(fill="x", pady=(15, 10))
        ctk.CTkLabel(parent, text="系统日志 / SYSTEM LOG:", font=ctk.CTkFont(family="Courier", size=11),
                     text_color="#a78bfa", anchor="w").pack(fill="x")

        self.log_frame = ctk.CTkFrame(parent, fg_color="transparent", height=100)
        self.log_frame.pack(fill="x", pady=(5, 0))
        self.log_frame.pack_propagate(False)

        self.log_labels = []
        logs = ["✓ AI课程模块加载完成", "✓ 提示词引擎初始化成功", "✓ AWS Skill Builder连接就绪",
                "⏳ 等待学员登录...", "🔐 安全通道已启用"]
        for log in logs:
            lbl = ctk.CTkLabel(self.log_frame, text=log, font=ctk.CTkFont(family="Courier", size=10),
                              text_color="#10b981", anchor="w")
            lbl.pack(fill="x")
            self.log_labels.append(lbl)
    
    def _create_footer(self, parent):
        ctk.CTkFrame(parent, height=1, fg_color="#5b21b6").pack(fill="x", pady=(15, 8))
        ctk.CTkLabel(parent, text="© 2024 提示词工程课程实训平台 | AWS Skill Builder",
                     font=ctk.CTkFont(size=9), text_color="#6b4fc3").pack()
    
    def _start_log_animation(self):
        def blink():
            for lbl in self.log_labels:
                lbl.configure(text_color="#10b981" if random.random() > 0.3 else "#065f46")
            self.after(500, blink)
        blink()
    
    def _add_log(self, text):
        for i in range(len(self.log_labels) - 1):
            self.log_labels[i].configure(text=self.log_labels[i + 1].cget("text"))
        self.log_labels[-1].configure(text=text)
    
    def _handle_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("⚠ 提示", "请输入学员账号和密码")
            return

        self.login_btn.configure(state="disabled", text="🔄  正在登录...")
        self._add_log("⏳ 正在打开课程平台...")
        
        def login_task():
            try:
                self.login_service.login(username, password)
                self.after(0, self._on_success)
            except Exception as e:
                self.after(0, lambda: self._on_error(str(e)))
        
        threading.Thread(target=login_task, daemon=True).start()
    
    def _on_success(self):
        self._add_log("✓ 登录成功！正在跳转课程平台...")
        self.login_btn.configure(state="normal", text="🚀  进入课程平台 / LOGIN")

    def _on_error(self, msg):
        self._add_log(f"✖ 错误: {msg[:30]}")
        self.login_btn.configure(state="normal", text="🚀  进入课程平台 / LOGIN")
        messagebox.showerror("✖ 登录失败", msg)
