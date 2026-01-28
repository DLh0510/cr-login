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
        self.role = "student"
        self._setup_window()
        self._create_ui()
    
    def _setup_window(self):
        self.title(CONFIG['title'])
        self.geometry("420x580")
        self.resizable(False, False)
        self.configure(fg_color="#1a1b2e")
        ctk.set_appearance_mode("dark")
    
    def _create_ui(self):
        # 主卡片
        card = ctk.CTkFrame(self, fg_color="#252742", corner_radius=16)
        card.pack(padx=20, pady=20, fill="both", expand=True)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=25, pady=25)
        
        # 头部：Logo + 标题
        header = ctk.CTkFrame(inner, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        # Logo
        try:
            img = ctk.CTkImage(Image.open(resource_path(CONFIG["logo_file"])), size=(50, 50))
            ctk.CTkLabel(header, image=img, text="").pack(side="left", padx=(0, 12))
        except:
            logo_frame = ctk.CTkFrame(header, fg_color="#6366f1", width=50, height=50, corner_radius=12)
            logo_frame.pack(side="left", padx=(0, 12))
            logo_frame.pack_propagate(False)
            ctk.CTkLabel(logo_frame, text="☁", font=ctk.CTkFont(size=24), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
        
        # 标题
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="y")
        ctk.CTkLabel(title_frame, text=CONFIG["title"], font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="white", anchor="w").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="实训平台 v4.3", font=ctk.CTkFont(size=11),
                     text_color="#8b8ca7", anchor="w").pack(anchor="w")
        
        # 用户名
        ctk.CTkLabel(inner, text="USERNAME / 用户名", font=ctk.CTkFont(size=11),
                     text_color="#8b8ca7", anchor="w").pack(fill="x", pady=(0, 6))
        
        user_frame = ctk.CTkFrame(inner, fg_color="#1e1f36", corner_radius=10, height=50)
        user_frame.pack(fill="x", pady=(0, 16))
        user_frame.pack_propagate(False)
        uf = ctk.CTkFrame(user_frame, fg_color="transparent")
        uf.pack(fill="both", expand=True, padx=15)
        ctk.CTkLabel(uf, text="👤", font=ctk.CTkFont(size=16), text_color="#6b6c87").pack(side="left")
        self.user_entry = ctk.CTkEntry(uf, placeholder_text="请输入用户名", border_width=0,
                                       fg_color="transparent", text_color="white",
                                       placeholder_text_color="#6b6c87", font=ctk.CTkFont(size=13))
        self.user_entry.pack(side="left", fill="x", expand=True, padx=10)
        
        # 密码
        ctk.CTkLabel(inner, text="PASSWORD / 访问密钥", font=ctk.CTkFont(size=11),
                     text_color="#8b8ca7", anchor="w").pack(fill="x", pady=(0, 6))
        
        pass_frame = ctk.CTkFrame(inner, fg_color="#1e1f36", corner_radius=10, height=50)
        pass_frame.pack(fill="x", pady=(0, 20))
        pass_frame.pack_propagate(False)
        pf = ctk.CTkFrame(pass_frame, fg_color="transparent")
        pf.pack(fill="both", expand=True, padx=15)
        ctk.CTkLabel(pf, text="🔑", font=ctk.CTkFont(size=16), text_color="#6b6c87").pack(side="left")
        self.pass_entry = ctk.CTkEntry(pf, placeholder_text="请输入密码", border_width=0,
                                       fg_color="transparent", text_color="white",
                                       placeholder_text_color="#6b6c87", font=ctk.CTkFont(size=13), show="●")
        self.pass_entry.pack(side="left", fill="x", expand=True, padx=10)
        
        # 角色切换
        role_frame = ctk.CTkFrame(inner, fg_color="transparent")
        role_frame.pack(fill="x", pady=(0, 20))
        
        self.student_btn = ctk.CTkButton(role_frame, text="🎓 学生", height=45, corner_radius=10,
                                         font=ctk.CTkFont(size=13), fg_color="#1e1f36", text_color="white",
                                         border_width=1, border_color="#6366f1",
                                         hover_color="#2d2e4a", command=lambda: self._select_role("student"))
        self.student_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))
        
        self.teacher_btn = ctk.CTkButton(role_frame, text="👨‍🏫 教师", height=45, corner_radius=10,
                                         font=ctk.CTkFont(size=13), fg_color="#1e1f36", text_color="#8b8ca7",
                                         border_width=1, border_color="#3d3e5c",
                                         hover_color="#2d2e4a", command=lambda: self._select_role("teacher"))
        self.teacher_btn.pack(side="left", fill="x", expand=True, padx=(6, 0))
        
        # 登录按钮 - 渐变效果用纯色模拟
        self.login_btn = ctk.CTkButton(inner, text="登 录 平 台  →", height=55, corner_radius=12,
                                       font=ctk.CTkFont(size=15, weight="bold"),
                                       fg_color="#a855f7", hover_color="#9333ea",
                                       command=self._handle_login)
        self.login_btn.pack(fill="x", pady=(0, 15))
        self.pass_entry.bind('<Return>', lambda e: self._handle_login())
        
        # 分隔线
        ctk.CTkFrame(inner, fg_color="#3d3e5c", height=1).pack(fill="x", pady=(0, 15))
        
        # 底部提示
        tip_frame = ctk.CTkFrame(inner, fg_color="#1e1f36", corner_radius=8)
        tip_frame.pack(fill="x")
        ctk.CTkLabel(tip_frame, text="⚠️ 请通过官方渠道获取凭证，严禁分享账号密钥。",
                     font=ctk.CTkFont(size=10), text_color="#f59e0b",
                     wraplength=320).pack(padx=15, pady=10)
    
    def _select_role(self, role):
        self.role = role
        if role == "student":
            self.student_btn.configure(border_color="#6366f1", text_color="white")
            self.teacher_btn.configure(border_color="#3d3e5c", text_color="#8b8ca7")
        else:
            self.teacher_btn.configure(border_color="#6366f1", text_color="white")
            self.student_btn.configure(border_color="#3d3e5c", text_color="#8b8ca7")
    
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
        self.login_btn.configure(state="normal", text="登 录 平 台  →")
    
    def _on_error(self, msg):
        self.login_btn.configure(state="normal", text="登 录 平 台  →")
        messagebox.showerror("登录失败", msg)
