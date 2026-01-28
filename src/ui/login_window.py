"""登录窗口 - 云计算技能大赛"""
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
        ctk.CTkLabel(left, text="云计算技能大赛训练平台", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="white").pack(pady=(0, 8))
        ctk.CTkLabel(left, text=CONFIG["subtitle"], font=ctk.CTkFont(size=11),
                     text_color="#64748b").pack(pady=(0, 25))
        
        # 技术标签
        tags_frame = ctk.CTkFrame(left, fg_color="transparent")
        tags_frame.pack()
        tags = ["AWS", "CloudRaiser", "EC2", "S3", "Lambda"]
        row1 = ctk.CTkFrame(tags_frame, fg_color="transparent")
        row1.pack(pady=3)
        row2 = ctk.CTkFrame(tags_frame, fg_color="transparent")
        row2.pack(pady=3)
        
        for tag in tags[:3]:
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
        inner.pack(fill="both", expand=True, padx=32, pady=24)
        
        # 头部
        header = ctk.CTkFrame(inner, fg_color="transparent")
        header.pack(fill="x", pady=(0, 5))
        try:
            img = ctk.CTkImage(Image.open(resource_path(CONFIG["logo_file"])), size=(36, 36))
            ctk.CTkLabel(header, image=img, text="").pack(side="left", padx=(0, 10))
        except: pass
        ctk.CTkLabel(header, text="河南经济贸易技师学院", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="white").pack(side="left")
        
        ctk.CTkLabel(inner, text="欢迎参加技能大赛", font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="white").pack(anchor="w", pady=(12, 3))
        ctk.CTkLabel(inner, text="请输入您的凭证以访问训练平台", font=ctk.CTkFont(size=11),
                     text_color="#64748b").pack(anchor="w", pady=(0, 14))
        
        # EventCode
        ctk.CTkLabel(inner, text="EventCode", font=ctk.CTkFont(size=11), text_color="#94a3b8", anchor="w").pack(fill="x", pady=(0, 4))
        self.event_entry = ctk.CTkEntry(inner, height=40, corner_radius=10, fg_color="#0f172a",
                                        border_width=1, border_color="#334155", text_color="white",
                                        placeholder_text="输入活动代码", placeholder_text_color="#475569")
        self.event_entry.pack(fill="x", pady=(0, 10))
        
        # ID
        ctk.CTkLabel(inner, text="ID", font=ctk.CTkFont(size=11), text_color="#94a3b8", anchor="w").pack(fill="x", pady=(0, 4))
        self.user_entry = ctk.CTkEntry(inner, height=40, corner_radius=10, fg_color="#0f172a",
                                       border_width=1, border_color="#334155", text_color="white",
                                       placeholder_text="输入账号", placeholder_text_color="#475569")
        self.user_entry.pack(fill="x", pady=(0, 10))
        
        # Password
        ctk.CTkLabel(inner, text="Password", font=ctk.CTkFont(size=11), text_color="#94a3b8", anchor="w").pack(fill="x", pady=(0, 4))
        self.pass_entry = ctk.CTkEntry(inner, height=40, corner_radius=10, fg_color="#0f172a",
                                       border_width=1, border_color="#334155", text_color="white",
                                       placeholder_text="输入密码", placeholder_text_color="#475569", show="●")
        self.pass_entry.pack(fill="x", pady=(0, 10))
        
        # Player Name
        ctk.CTkLabel(inner, text="Player Name", font=ctk.CTkFont(size=11), text_color="#94a3b8", anchor="w").pack(fill="x", pady=(0, 4))
        self.name_entry = ctk.CTkEntry(inner, height=40, corner_radius=10, fg_color="#0f172a",
                                       border_width=1, border_color="#334155", text_color="white",
                                       placeholder_text="输入选手姓名", placeholder_text_color="#475569")
        self.name_entry.pack(fill="x", pady=(0, 14))
        
        # 登录按钮
        self.login_btn = ctk.CTkButton(inner, text="进入训练平台 →", height=44, corner_radius=10,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       fg_color="#00f5ff", hover_color="#00d4e6", text_color="#020617",
                                       command=self._handle_login)
        self.login_btn.pack(fill="x")
        self.name_entry.bind('<Return>', lambda e: self._handle_login())
    
    def _handle_login(self):
        event_code = self.event_entry.get().strip()
        user_id = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        player_name = self.name_entry.get().strip()
        
        if not all([event_code, user_id, password, player_name]):
            messagebox.showwarning("提示", "请填写所有字段")
            return
        
        self.login_btn.configure(state="disabled", text="登录中...")
        self.login_service = LoginService(CONFIG["login_url"])
        
        def task():
            try:
                self.login_service.login(event_code, user_id, password, player_name)
                self.after(0, lambda: self.login_btn.configure(state="normal", text="进入训练平台 →"))
            except Exception as e:
                self.after(0, lambda: [self.login_btn.configure(state="normal", text="进入训练平台 →"),
                                       messagebox.showerror("登录失败", str(e))])
        
        threading.Thread(target=task, daemon=True).start()
