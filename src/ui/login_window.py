"""登录窗口 - 双栏布局"""
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
        self.geometry("820x500")
        self.resizable(False, False)
        self.configure(fg_color="#0a0e27")
        ctk.set_appearance_mode("dark")
    
    def _create_ui(self):
        main = ctk.CTkFrame(self, fg_color="#0f1629", corner_radius=16)
        main.pack(padx=15, pady=15, fill="both", expand=True)
        
        # 左侧
        left = ctk.CTkFrame(main, fg_color="transparent", width=350)
        left.pack(side="left", fill="both", padx=30, pady=30)
        left.pack_propagate(False)
        
        # 状态
        status = ctk.CTkFrame(left, fg_color="#1a2234", corner_radius=15)
        status.pack(anchor="w")
        sf = ctk.CTkFrame(status, fg_color="transparent")
        sf.pack(padx=12, pady=6)
        ctk.CTkLabel(sf, text="●", font=ctk.CTkFont(size=10), text_color="#22c55e").pack(side="left")
        ctk.CTkLabel(sf, text=" PLATFORM ONLINE", font=ctk.CTkFont(size=11), text_color="#22c55e").pack(side="left")
        
        # 大标题
        ctk.CTkLabel(left, text="云计算", font=ctk.CTkFont(size=48, weight="bold"),
                     text_color="#00d4ff").pack(anchor="w", pady=(20, 0))
        ctk.CTkLabel(left, text="无服务器架构竞赛平台", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white").pack(anchor="w", pady=(0, 12))
        
        ctk.CTkLabel(left, text="WorldSkills 技术标准 · Serverless 架构实训\n自动化评分系统 · 企业级云原生实践",
                     font=ctk.CTkFont(size=12), text_color="#94a3b8", justify="left").pack(anchor="w", pady=(0, 20))
        
        # Logo 展示
        logos_frame = ctk.CTkFrame(left, fg_color="transparent")
        logos_frame.pack(anchor="w", pady=(0, 20))
        
        try:
            ws_img = ctk.CTkImage(Image.open(resource_path("worldskills_logo.png")), size=(100, 40))
            ctk.CTkLabel(logos_frame, image=ws_img, text="").pack(side="left", padx=(0, 15))
        except:
            pass
        
        try:
            aws_img = ctk.CTkImage(Image.open(resource_path("aws_logo.png")), size=(40, 40))
            ctk.CTkLabel(logos_frame, image=aws_img, text="").pack(side="left", padx=(0, 15))
        except:
            pass
        
        # 指标
        metrics = ctk.CTkFrame(left, fg_color="transparent")
        metrics.pack(anchor="w")
        for val, label in [("99.9%", "SLA可用性"), ("Lambda", "无服务器"), ("S3", "对象存储")]:
            m = ctk.CTkFrame(metrics, fg_color="#1a2234", corner_radius=8, width=90, height=60)
            m.pack(side="left", padx=(0, 8))
            m.pack_propagate(False)
            ctk.CTkLabel(m, text=val, font=ctk.CTkFont(size=15, weight="bold"), text_color="#00d4ff").pack(pady=(10, 2))
            ctk.CTkLabel(m, text=label, font=ctk.CTkFont(size=9), text_color="#64748b").pack()
        
        # 右侧登录卡片
        right = ctk.CTkFrame(main, fg_color="#1a2234", corner_radius=16, width=340)
        right.pack(side="right", fill="y", padx=(0, 15), pady=15)
        right.pack_propagate(False)
        
        inner = ctk.CTkFrame(right, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=28, pady=25)
        
        # 头部
        header = ctk.CTkFrame(inner, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        try:
            img = ctk.CTkImage(Image.open(resource_path(CONFIG["logo_file"])), size=(40, 40))
            ctk.CTkLabel(header, image=img, text="").pack(side="left", padx=(0, 10))
        except:
            logo = ctk.CTkFrame(header, fg_color="#00d4ff", width=40, height=40, corner_radius=10)
            logo.pack(side="left", padx=(0, 10))
            logo.pack_propagate(False)
            ctk.CTkLabel(logo, text="☁", font=ctk.CTkFont(size=18), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(header, text="河南经济贸易技师学院", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="white").pack(side="left")
        
        # 用户名
        ctk.CTkLabel(inner, text="账号 / ID", font=ctk.CTkFont(size=10), text_color="#94a3b8", anchor="w").pack(fill="x", pady=(0, 5))
        self.user_entry = ctk.CTkEntry(inner, height=42, corner_radius=10, fg_color="#0f1629",
                                       border_width=1, border_color="#334155", text_color="white",
                                       placeholder_text="请输入用户名", placeholder_text_color="#475569")
        self.user_entry.pack(fill="x", pady=(0, 12))
        
        # 密码
        ctk.CTkLabel(inner, text="密码 / Password", font=ctk.CTkFont(size=10), text_color="#94a3b8", anchor="w").pack(fill="x", pady=(0, 5))
        self.pass_entry = ctk.CTkEntry(inner, height=42, corner_radius=10, fg_color="#0f1629",
                                       border_width=1, border_color="#334155", text_color="white",
                                       placeholder_text="请输入密码", placeholder_text_color="#475569", show="●")
        self.pass_entry.pack(fill="x", pady=(0, 15))
        
        # 角色
        role_f = ctk.CTkFrame(inner, fg_color="transparent")
        role_f.pack(fill="x", pady=(0, 15))
        self.student_btn = ctk.CTkButton(role_f, text="🎓 学生", height=38, corner_radius=8,
                                         font=ctk.CTkFont(size=12), fg_color="#0f1629",
                                         border_width=1, border_color="#00d4ff", text_color="white",
                                         hover_color="#1a2845", command=lambda: self._select_role("student"))
        self.student_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        
        self.teacher_btn = ctk.CTkButton(role_f, text="👨‍🏫 老师", height=38, corner_radius=8,
                                         font=ctk.CTkFont(size=12), fg_color="#0f1629",
                                         border_width=1, border_color="#334155", text_color="#94a3b8",
                                         hover_color="#1a2845", command=lambda: self._select_role("teacher"))
        self.teacher_btn.pack(side="left", fill="x", expand=True, padx=(4, 0))
        
        # 登录按钮
        self.login_btn = ctk.CTkButton(inner, text="进入实训平台 →", height=45, corner_radius=10,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       fg_color="#00d4ff", hover_color="#00b8e6", text_color="#0a0e27",
                                       command=self._handle_login)
        self.login_btn.pack(fill="x")
        self.pass_entry.bind('<Return>', lambda e: self._handle_login())
    
    def _select_role(self, role):
        self.role = role
        if role == "student":
            self.student_btn.configure(border_color="#00d4ff", text_color="white")
            self.teacher_btn.configure(border_color="#334155", text_color="#94a3b8")
        else:
            self.teacher_btn.configure(border_color="#00d4ff", text_color="white")
            self.student_btn.configure(border_color="#334155", text_color="#94a3b8")
    
    def _handle_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("提示", "请输入用户名和密码")
            return
        
        url = CONFIG["teacher_url"] if self.role == "teacher" else CONFIG["student_url"]
        self.login_btn.configure(state="disabled", text="登录中...")
        self.login_service = LoginService(url)
        
        def task():
            try:
                self.login_service.login(username, password)
                self.after(0, lambda: self.login_btn.configure(state="normal", text="进入实训平台 →"))
            except Exception as e:
                self.after(0, lambda: [self.login_btn.configure(state="normal", text="进入实训平台 →"),
                                       messagebox.showerror("登录失败", str(e))])
        
        threading.Thread(target=task, daemon=True).start()
