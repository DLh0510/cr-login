"""登录窗口 - 教师/学生双入口"""
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
        self.role = "teacher"
        self._setup_window()
        self._create_ui()
        self._start_log_animation()
    
    def _setup_window(self):
        self.title(CONFIG['title'])
        self.geometry(CONFIG["window_size"])
        self.resizable(False, False)
        self.configure(fg_color="#0a0e14")
        ctk.set_appearance_mode("dark")
    
    def _create_ui(self):
        main = ctk.CTkFrame(self, fg_color="#0a0e14", border_width=1, border_color="#00d4ff", corner_radius=0)
        main.pack(expand=True, fill="both", padx=15, pady=15)
        
        ctk.CTkFrame(main, height=2, fg_color="#00d4ff").pack(fill="x", pady=(10,0))
        
        content = ctk.CTkFrame(main, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=25, pady=20)
        
        self._create_header(content)
        self._create_role_selector(content)
        self._create_form(content)
        self._create_log_panel(content)
        self._create_footer(content)
    
    def _create_header(self, parent):
        try:
            img = ctk.CTkImage(Image.open(resource_path(CONFIG["logo_file"])), size=(70, 70))
            ctk.CTkLabel(parent, image=img, text="").pack(pady=(5, 10))
        except:
            ctk.CTkLabel(parent, text="🎓", font=ctk.CTkFont(size=50)).pack(pady=(5, 10))
        
        ctk.CTkLabel(parent, text=CONFIG["title"], font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#00d4ff").pack(pady=(0, 15))
    
    def _create_role_selector(self, parent):
        role_frame = ctk.CTkFrame(parent, fg_color="transparent")
        role_frame.pack(fill="x", pady=(0, 15))
        
        self.teacher_btn = ctk.CTkButton(role_frame, text="👨‍🏫 教师登录", width=180, height=40, corner_radius=6,
                                         font=ctk.CTkFont(size=13, weight="bold"),
                                         fg_color="#00d4ff", text_color="#0a0e14",
                                         command=lambda: self._select_role("teacher"))
        self.teacher_btn.pack(side="left", padx=(0, 10))
        
        self.student_btn = ctk.CTkButton(role_frame, text="👨‍🎓 学生登录", width=180, height=40, corner_radius=6,
                                         font=ctk.CTkFont(size=13, weight="bold"),
                                         fg_color="#1e3a5f", text_color="#4a9eff",
                                         command=lambda: self._select_role("student"))
        self.student_btn.pack(side="right")
    
    def _select_role(self, role):
        self.role = role
        if role == "teacher":
            self.teacher_btn.configure(fg_color="#00d4ff", text_color="#0a0e14")
            self.student_btn.configure(fg_color="#1e3a5f", text_color="#4a9eff")
        else:
            self.student_btn.configure(fg_color="#00d4ff", text_color="#0a0e14")
            self.teacher_btn.configure(fg_color="#1e3a5f", text_color="#4a9eff")
    
    def _create_form(self, parent):
        form = ctk.CTkFrame(parent, fg_color="transparent")
        form.pack(fill="x", pady=5)
        
        self.user_entry = self._create_input(form, "账号", "user")
        self.pass_entry = self._create_input(form, "密码", "pass", show="●")
        
        self.login_btn = ctk.CTkButton(form, text="⟳  登 录", height=45, corner_radius=4,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       fg_color="#00d4ff", hover_color="#00a8cc", text_color="#0a0e14",
                                       command=self._handle_login)
        self.login_btn.pack(fill="x", pady=(10, 0))
        self.pass_entry.bind('<Return>', lambda e: self._handle_login())
    
    def _create_input(self, parent, placeholder, name, show=None):
        frame = ctk.CTkFrame(parent, fg_color="#0d1117", border_width=1, border_color="#1e3a5f", corner_radius=4)
        frame.pack(fill="x", pady=(0, 12))
        
        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=8)
        
        entry = ctk.CTkEntry(inner, placeholder_text=placeholder, border_width=0, fg_color="transparent",
                            text_color="#00d4ff", placeholder_text_color="#3d5a80", font=ctk.CTkFont(size=13),
                            height=30, show=show)
        entry.pack(side="left", fill="x", expand=True)
        
        icon = "👤" if name == "user" else "🔒"
        ctk.CTkLabel(inner, text=icon, font=ctk.CTkFont(size=16), text_color="#3d5a80").pack(side="right")
        return entry
    
    def _create_log_panel(self, parent):
        ctk.CTkFrame(parent, height=1, fg_color="#1e3a5f").pack(fill="x", pady=(15, 10))
        ctk.CTkLabel(parent, text="SYSTEM LOG:", font=ctk.CTkFont(family="Courier", size=11),
                     text_color="#4a9eff", anchor="w").pack(fill="x")
        
        self.log_frame = ctk.CTkFrame(parent, fg_color="transparent", height=80)
        self.log_frame.pack(fill="x", pady=(5, 0))
        self.log_frame.pack_propagate(False)
        
        self.log_labels = []
        logs = ["> 系统就绪", "> 等待用户登录...", "> 加密通道已启用", "> 连接正常"]
        for log in logs:
            lbl = ctk.CTkLabel(self.log_frame, text=log, font=ctk.CTkFont(family="Courier", size=10),
                              text_color="#00ff88", anchor="w")
            lbl.pack(fill="x")
            self.log_labels.append(lbl)
    
    def _create_footer(self, parent):
        ctk.CTkFrame(parent, height=1, fg_color="#1e3a5f").pack(fill="x", pady=(15, 8))
        ctk.CTkLabel(parent, text="SECURE CONNECTION | TLS ENCRYPTED",
                     font=ctk.CTkFont(family="Courier", size=9), text_color="#3d5a80").pack()
    
    def _start_log_animation(self):
        def blink():
            for lbl in self.log_labels:
                lbl.configure(text_color="#00ff88" if random.random() > 0.3 else "#004422")
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
            messagebox.showwarning("提示", "请输入账号和密码")
            return
        
        url = CONFIG["teacher_url"] if self.role == "teacher" else CONFIG["student_url"]
        role_name = "教师" if self.role == "teacher" else "学生"
        
        self.login_btn.configure(state="disabled", text="⟳  登录中...")
        self._add_log(f"> 正在以{role_name}身份登录...")
        
        self.login_service = LoginService(url)
        
        def login_task():
            try:
                self.login_service.login(username, password)
                self.after(0, self._on_success)
            except Exception as e:
                self.after(0, lambda: self._on_error(str(e)))
        
        threading.Thread(target=login_task, daemon=True).start()
    
    def _on_success(self):
        self._add_log("> ✓ 登录成功")
        self.login_btn.configure(state="normal", text="⟳  登 录")
    
    def _on_error(self, msg):
        self._add_log(f"> ✖ 错误: {msg[:25]}")
        self.login_btn.configure(state="normal", text="⟳  登 录")
        messagebox.showerror("登录失败", msg)
