"""登录窗口 - 容器技术风格"""
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
        self.geometry(CONFIG["window_size"])
        self.resizable(False, False)
        self.configure(fg_color="#020617")
        ctk.set_appearance_mode("dark")
    
    def _create_ui(self):
        main = ctk.CTkFrame(self, fg_color="#0f172a", corner_radius=0)
        main.pack(fill="both", expand=True)
        
        # 左侧品牌区
        left = ctk.CTkFrame(main, fg_color="transparent", width=380)
        left.pack(side="left", fill="both", padx=40, pady=40)
        left.pack_propagate(False)
        
        # 云计算图标框
        cube = ctk.CTkFrame(left, fg_color="#0f172a", width=80, height=80, corner_radius=8,
                           border_width=2, border_color="#00f5ff")
        cube.pack(pady=(20, 25))
        cube.pack_propagate(False)
        ctk.CTkLabel(cube, text="云计算", font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#00f5ff").place(relx=0.5, rely=0.5, anchor="center")
        
        # 大标题
        ctk.CTkLabel(left, text="云计算容器技术与应用实训平台", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="white").pack(pady=(0, 8))
        ctk.CTkLabel(left, text=CONFIG["subtitle"], font=ctk.CTkFont(size=12),
                     text_color="#64748b").pack(pady=(0, 25))
        
        # 技术标签
        tags_frame = ctk.CTkFrame(left, fg_color="transparent")
        tags_frame.pack()
        tags = ["Docker", "Kubernetes", "Microservices", "DevOps", "CI/CD"]
        row1 = ctk.CTkFrame(tags_frame, fg_color="transparent")
        row1.pack(pady=3)
        row2 = ctk.CTkFrame(tags_frame, fg_color="transparent")
        row2.pack(pady=3)
        
        for i, tag in enumerate(tags[:3]):
            t = ctk.CTkFrame(row1, fg_color="#1e293b", corner_radius=15, border_width=1, border_color="#334155")
            t.pack(side="left", padx=4)
            ctk.CTkLabel(t, text=tag, font=ctk.CTkFont(size=11), text_color="#94a3b8").pack(padx=12, pady=6)
        
        for tag in tags[3:]:
            t = ctk.CTkFrame(row2, fg_color="#1e293b", corner_radius=15, border_width=1, border_color="#334155")
            t.pack(side="left", padx=4)
            ctk.CTkLabel(t, text=tag, font=ctk.CTkFont(size=11), text_color="#94a3b8").pack(padx=12, pady=6)
        
        # Logo 展示
        logos_frame = ctk.CTkFrame(left, fg_color="transparent")
        logos_frame.pack(pady=(25, 0))
        try:
            ws_img = ctk.CTkImage(Image.open(resource_path("worldskills_logo.png")), size=(90, 36))
            ctk.CTkLabel(logos_frame, image=ws_img, text="").pack(side="left", padx=8)
        except: pass
        try:
            aws_img = ctk.CTkImage(Image.open(resource_path("aws_logo.png")), size=(36, 36))
            ctk.CTkLabel(logos_frame, image=aws_img, text="").pack(side="left", padx=8)
        except: pass
        
        # 第二行 logo
        logos_frame2 = ctk.CTkFrame(left, fg_color="transparent")
        logos_frame2.pack(pady=(10, 0))
        try:
            foot_img = ctk.CTkImage(Image.open(resource_path("foot_logo.png")), size=(120, 40))
            ctk.CTkLabel(logos_frame2, image=foot_img, text="").pack()
        except: pass
        
        # 右侧登录卡片
        right = ctk.CTkFrame(main, fg_color="#1e293b", corner_radius=20, width=360,
                            border_width=1, border_color="#334155")
        right.pack(side="right", fill="y", padx=(0, 30), pady=30)
        right.pack_propagate(False)
        
        inner = ctk.CTkFrame(right, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=32, pady=28)
        
        # 头部
        header = ctk.CTkFrame(inner, fg_color="transparent")
        header.pack(fill="x", pady=(0, 5))
        try:
            img = ctk.CTkImage(Image.open(resource_path(CONFIG["logo_file"])), size=(36, 36))
            ctk.CTkLabel(header, image=img, text="").pack(side="left", padx=(0, 10))
        except: pass
        ctk.CTkLabel(header, text="河南经济贸易技师学院", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="white").pack(side="left")
        
        ctk.CTkLabel(inner, text="欢迎回到实训平台", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white").pack(anchor="w", pady=(15, 3))
        ctk.CTkLabel(inner, text="请输入您的凭证以访问实训平台", font=ctk.CTkFont(size=11),
                     text_color="#64748b").pack(anchor="w", pady=(0, 18))
        
        # 用户名
        ctk.CTkLabel(inner, text="账号", font=ctk.CTkFont(size=11), text_color="#94a3b8", anchor="w").pack(fill="x", pady=(0, 5))
        self.user_entry = ctk.CTkEntry(inner, height=44, corner_radius=10, fg_color="#0f172a",
                                       border_width=1, border_color="#334155", text_color="white",
                                       placeholder_text="输入账号", placeholder_text_color="#475569")
        self.user_entry.pack(fill="x", pady=(0, 14))
        
        # 密码
        ctk.CTkLabel(inner, text="密码", font=ctk.CTkFont(size=11), text_color="#94a3b8", anchor="w").pack(fill="x", pady=(0, 5))
        self.pass_entry = ctk.CTkEntry(inner, height=44, corner_radius=10, fg_color="#0f172a",
                                       border_width=1, border_color="#334155", text_color="white",
                                       placeholder_text="输入密码", placeholder_text_color="#475569", show="●")
        self.pass_entry.pack(fill="x", pady=(0, 14))
        
        # 角色
        role_f = ctk.CTkFrame(inner, fg_color="transparent")
        role_f.pack(fill="x", pady=(0, 16))
        self.student_btn = ctk.CTkButton(role_f, text="🎓 学生", height=38, corner_radius=8,
                                         font=ctk.CTkFont(size=12), fg_color="#0f172a",
                                         border_width=1, border_color="#00f5ff", text_color="white",
                                         hover_color="#1e3a5a", command=lambda: self._select_role("student"))
        self.student_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        
        self.teacher_btn = ctk.CTkButton(role_f, text="👨‍🏫 老师", height=38, corner_radius=8,
                                         font=ctk.CTkFont(size=12), fg_color="#0f172a",
                                         border_width=1, border_color="#334155", text_color="#64748b",
                                         hover_color="#1e3a5a", command=lambda: self._select_role("teacher"))
        self.teacher_btn.pack(side="left", fill="x", expand=True, padx=(4, 0))
        
        # 登录按钮
        self.login_btn = ctk.CTkButton(inner, text="进入比赛平台 →", height=46, corner_radius=10,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       fg_color="#00f5ff", hover_color="#00d4e6", text_color="#020617",
                                       command=self._handle_login)
        self.login_btn.pack(fill="x")
        self.pass_entry.bind('<Return>', lambda e: self._handle_login())
    
    def _select_role(self, role):
        self.role = role
        if role == "student":
            self.student_btn.configure(border_color="#00f5ff", text_color="white")
            self.teacher_btn.configure(border_color="#334155", text_color="#64748b")
        else:
            self.teacher_btn.configure(border_color="#00f5ff", text_color="white")
            self.student_btn.configure(border_color="#334155", text_color="#64748b")
    
    def _handle_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("提示", "请输入用户名和密码")
            return
        
        url = CONFIG["teacher_url"] if self.role == "teacher" else CONFIG["student_url"]
        self.login_btn.configure(state="disabled", text="验证中...")
        self.login_service = LoginService(url)
        
        def task():
            try:
                self.login_service.login(username, password)
                self.after(0, lambda: self.login_btn.configure(state="normal", text="进入比赛平台 →"))
            except Exception as e:
                self.after(0, lambda: [self.login_btn.configure(state="normal", text="进入比赛平台 →"),
                                       messagebox.showerror("登录失败", str(e))])
        
        threading.Thread(target=task, daemon=True).start()
