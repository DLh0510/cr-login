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
        self.geometry("820x520")
        self.resizable(False, False)
        self.configure(fg_color="#0f1219")
        ctk.set_appearance_mode("dark")
    
    def _create_ui(self):
        # 主容器
        main = ctk.CTkFrame(self, fg_color="#181c28", corner_radius=12)
        main.pack(padx=15, pady=15, fill="both", expand=True)
        
        # 左侧信息区
        left = ctk.CTkFrame(main, fg_color="transparent", width=350)
        left.pack(side="left", fill="both", padx=30, pady=30)
        left.pack_propagate(False)
        
        # 在线状态
        status_frame = ctk.CTkFrame(left, fg_color="#1e2433", corner_radius=15, height=30)
        status_frame.pack(anchor="w")
        status_inner = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_inner.pack(padx=12, pady=6)
        ctk.CTkLabel(status_inner, text="●", font=ctk.CTkFont(size=10), text_color="#22c55e").pack(side="left")
        ctk.CTkLabel(status_inner, text=" PLATFORM ONLINE", font=ctk.CTkFont(size=11),
                     text_color="#22c55e").pack(side="left")
        
        # 大标题
        ctk.CTkLabel(left, text="云计算", font=ctk.CTkFont(size=48, weight="bold"),
                     text_color="#a855f7").pack(anchor="w", pady=(25, 0))
        ctk.CTkLabel(left, text="公有架构竞赛平台", font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="white").pack(anchor="w", pady=(0, 15))
        
        # 描述
        ctk.CTkLabel(left, text="WorldSkills 技术标准 · 企业级云架构实训 · 自动化评分系统",
                     font=ctk.CTkFont(size=12), text_color="#8b8ca7", wraplength=300,
                     justify="left").pack(anchor="w", pady=(0, 8))
        ctk.CTkLabel(left, text="🛡 符合 ISO 27001 安全合规标准",
                     font=ctk.CTkFont(size=11), text_color="#6b7280").pack(anchor="w", pady=(0, 25))
        
        # 指标卡片
        metrics = ctk.CTkFrame(left, fg_color="transparent")
        metrics.pack(anchor="w", fill="x")
        
        for value, label in [("99.9%", "SLA 可用性"), ("3+X", "云厂商支持"), ("IaC", "基础设施即代码")]:
            m = ctk.CTkFrame(metrics, fg_color="#1e2433", corner_radius=8, width=95, height=70)
            m.pack(side="left", padx=(0, 10))
            m.pack_propagate(False)
            ctk.CTkLabel(m, text=value, font=ctk.CTkFont(size=18, weight="bold"),
                        text_color="#a855f7").pack(pady=(12, 2))
            ctk.CTkLabel(m, text=label, font=ctk.CTkFont(size=9), text_color="#6b7280").pack()
        
        # 右侧登录卡片
        right = ctk.CTkFrame(main, fg_color="#252742", corner_radius=12, width=350)
        right.pack(side="right", fill="y", padx=(0, 15), pady=15)
        right.pack_propagate(False)
        
        inner = ctk.CTkFrame(right, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=25, pady=20)
        
        # 头部
        header = ctk.CTkFrame(inner, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        try:
            img = ctk.CTkImage(Image.open(resource_path(CONFIG["logo_file"])), size=(40, 40))
            ctk.CTkLabel(header, image=img, text="").pack(side="left", padx=(0, 10))
        except:
            logo = ctk.CTkFrame(header, fg_color="#6366f1", width=40, height=40, corner_radius=10)
            logo.pack(side="left", padx=(0, 10))
            logo.pack_propagate(False)
            ctk.CTkLabel(logo, text="☁", font=ctk.CTkFont(size=18), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
        
        title_f = ctk.CTkFrame(header, fg_color="transparent")
        title_f.pack(side="left")
        ctk.CTkLabel(title_f, text="河南经济贸易技师学院", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="white").pack(anchor="w")
        
        # 用户名
        ctk.CTkLabel(inner, text="USERNAME / 选手编号", font=ctk.CTkFont(size=10),
                     text_color="#8b8ca7", anchor="w").pack(fill="x", pady=(0, 5))
        user_f = ctk.CTkFrame(inner, fg_color="#1e1f36", corner_radius=8, height=45)
        user_f.pack(fill="x", pady=(0, 12))
        user_f.pack_propagate(False)
        uf = ctk.CTkFrame(user_f, fg_color="transparent")
        uf.pack(fill="both", expand=True, padx=12)
        ctk.CTkLabel(uf, text="👤", font=ctk.CTkFont(size=14), text_color="#6b6c87").pack(side="left")
        self.user_entry = ctk.CTkEntry(uf, placeholder_text="请输入用户名", border_width=0,
                                       fg_color="transparent", text_color="white",
                                       placeholder_text_color="#6b6c87", font=ctk.CTkFont(size=12))
        self.user_entry.pack(side="left", fill="x", expand=True, padx=8)
        
        # 密码
        ctk.CTkLabel(inner, text="PASSWORD / 访问密钥", font=ctk.CTkFont(size=10),
                     text_color="#8b8ca7", anchor="w").pack(fill="x", pady=(0, 5))
        pass_f = ctk.CTkFrame(inner, fg_color="#1e1f36", corner_radius=8, height=45)
        pass_f.pack(fill="x", pady=(0, 15))
        pass_f.pack_propagate(False)
        pf = ctk.CTkFrame(pass_f, fg_color="transparent")
        pf.pack(fill="both", expand=True, padx=12)
        ctk.CTkLabel(pf, text="🔑", font=ctk.CTkFont(size=14), text_color="#6b6c87").pack(side="left")
        self.pass_entry = ctk.CTkEntry(pf, placeholder_text="请输入密码", border_width=0,
                                       fg_color="transparent", text_color="white",
                                       placeholder_text_color="#6b6c87", font=ctk.CTkFont(size=12), show="●")
        self.pass_entry.pack(side="left", fill="x", expand=True, padx=8)
        
        # 角色
        role_f = ctk.CTkFrame(inner, fg_color="transparent")
        role_f.pack(fill="x", pady=(0, 15))
        self.student_btn = ctk.CTkButton(role_f, text="🎓 学生", height=40, corner_radius=8,
                                         font=ctk.CTkFont(size=12), fg_color="#1e1f36",
                                         border_width=1, border_color="#6366f1", text_color="white",
                                         hover_color="#2d2e4a", command=lambda: self._select_role("student"))
        self.student_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.teacher_btn = ctk.CTkButton(role_f, text="👨‍🏫 老师", height=40, corner_radius=8,
                                         font=ctk.CTkFont(size=12), fg_color="#1e1f36",
                                         border_width=1, border_color="#3d3e5c", text_color="#8b8ca7",
                                         hover_color="#2d2e4a", command=lambda: self._select_role("teacher"))
        self.teacher_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # 登录按钮
        self.login_btn = ctk.CTkButton(inner, text="登 录 平 台  →", height=50, corner_radius=10,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       fg_color="#a855f7", hover_color="#9333ea",
                                       command=self._handle_login)
        self.login_btn.pack(fill="x", pady=(0, 12))
        self.pass_entry.bind('<Return>', lambda e: self._handle_login())
        
        # 底部提示
        tip = ctk.CTkFrame(inner, fg_color="#1e1f36", corner_radius=6)
        tip.pack(fill="x")
        ctk.CTkLabel(tip, text="⚠️ 请通过官方渠道获取凭证，严禁分享账号密钥。",
                     font=ctk.CTkFont(size=9), text_color="#f59e0b", wraplength=260).pack(padx=10, pady=8)
    
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
        
        def task():
            try:
                self.login_service.login(username, password)
                self.after(0, lambda: self.login_btn.configure(state="normal", text="登 录 平 台  →"))
            except Exception as e:
                self.after(0, lambda: [self.login_btn.configure(state="normal", text="登 录 平 台  →"),
                                       messagebox.showerror("登录失败", str(e))])
        
        threading.Thread(target=task, daemon=True).start()
