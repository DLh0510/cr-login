"""登录窗口 - 教师/学生双入口"""
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import threading
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
    
    def _setup_window(self):
        self.title(CONFIG['title'])
        self.geometry("420x520")
        self.resizable(False, False)
        self.configure(fg_color="#f5f7fa")
        ctk.set_appearance_mode("light")
    
    def _create_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=40, pady=30)
        
        # Logo
        try:
            img = ctk.CTkImage(Image.open(resource_path(CONFIG["logo_file"])), size=(70, 70))
            ctk.CTkLabel(container, image=img, text="").pack(pady=(0, 10))
        except:
            pass
        
        # 标题
        ctk.CTkLabel(container, text=CONFIG["title"], font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#2d3748").pack(pady=(0, 20))
        
        # 登录卡片
        card = ctk.CTkFrame(container, fg_color="white", corner_radius=12,
                           border_width=1, border_color="#e2e8f0")
        card.pack(fill="x")
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=25, pady=25)
        
        # 角色切换
        role_frame = ctk.CTkFrame(inner, fg_color="#f1f5f9", corner_radius=8)
        role_frame.pack(fill="x", pady=(0, 20))
        
        rf = ctk.CTkFrame(role_frame, fg_color="transparent")
        rf.pack(padx=4, pady=4)
        
        self.teacher_btn = ctk.CTkButton(rf, text="👨‍🏫 教师", width=130, height=36, corner_radius=6,
                                         font=ctk.CTkFont(size=13), fg_color="#3b82f6", text_color="white",
                                         hover_color="#2563eb", command=lambda: self._select_role("teacher"))
        self.teacher_btn.pack(side="left", padx=(0, 4))
        
        self.student_btn = ctk.CTkButton(rf, text="👨‍🎓 学生", width=130, height=36, corner_radius=6,
                                         font=ctk.CTkFont(size=13), fg_color="transparent", text_color="#64748b",
                                         hover_color="#e2e8f0", command=lambda: self._select_role("student"))
        self.student_btn.pack(side="left")
        
        # 用户名
        ctk.CTkLabel(inner, text="用户名", font=ctk.CTkFont(size=12), text_color="#4a5568", anchor="w").pack(fill="x")
        self.user_entry = ctk.CTkEntry(inner, height=42, corner_radius=8, border_color="#e2e8f0",
                                       fg_color="#f8fafc", placeholder_text="请输入用户名",
                                       font=ctk.CTkFont(size=13))
        self.user_entry.pack(fill="x", pady=(4, 12))
        
        # 密码
        ctk.CTkLabel(inner, text="密码", font=ctk.CTkFont(size=12), text_color="#4a5568", anchor="w").pack(fill="x")
        self.pass_entry = ctk.CTkEntry(inner, height=42, corner_radius=8, border_color="#e2e8f0",
                                       fg_color="#f8fafc", placeholder_text="请输入密码",
                                       font=ctk.CTkFont(size=13), show="●")
        self.pass_entry.pack(fill="x", pady=(4, 16))
        
        # 登录按钮
        self.login_btn = ctk.CTkButton(inner, text="登 录", height=44, corner_radius=8,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       fg_color="#3b82f6", hover_color="#2563eb",
                                       command=self._handle_login)
        self.login_btn.pack(fill="x")
        self.pass_entry.bind('<Return>', lambda e: self._handle_login())
        
        # 底部
        ctk.CTkLabel(container, text="© 2024 云计算运维实训平台", font=ctk.CTkFont(size=10),
                     text_color="#94a3b8").pack(side="bottom", pady=(15, 0))
    
    def _select_role(self, role):
        self.role = role
        if role == "teacher":
            self.teacher_btn.configure(fg_color="#3b82f6", text_color="white")
            self.student_btn.configure(fg_color="transparent", text_color="#64748b")
        else:
            self.student_btn.configure(fg_color="#3b82f6", text_color="white")
            self.teacher_btn.configure(fg_color="transparent", text_color="#64748b")
    
    def _handle_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("提示", "请输入用户名和密码")
            return
        
        url = CONFIG["teacher_url"] if self.role == "teacher" else CONFIG["student_url"]
        
        self.login_btn.configure(state="disabled", text="登录中...")
        self.login_service = LoginService(url)
        
        def login_task():
            try:
                self.login_service.login(username, password)
                self.after(0, self._on_success)
            except Exception as e:
                self.after(0, lambda: self._on_error(str(e)))
        
        threading.Thread(target=login_task, daemon=True).start()
    
    def _on_success(self):
        self.login_btn.configure(state="normal", text="登 录")
    
    def _on_error(self, msg):
        self.login_btn.configure(state="normal", text="登 录")
        messagebox.showerror("登录失败", msg)
