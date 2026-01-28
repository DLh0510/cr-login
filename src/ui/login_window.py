"""登录窗口UI"""
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import threading
import os
import sys

from .theme import THEME
from ..config import CONFIG
from ..services.login_service import LoginService


def resource_path(path):
    """获取资源文件路径"""
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    return os.path.join(base, path)


class LoginWindow(ctk.CTk):
    """登录窗口"""
    
    def __init__(self):
        super().__init__()
        self.login_service = LoginService(CONFIG["url"])
        self._setup_window()
        self._create_ui()
    
    def _setup_window(self):
        """配置窗口"""
        self.title(f"{CONFIG['title']} - {CONFIG['subtitle']}")
        self.geometry(CONFIG["window_size"])
        self.resizable(False, False)
        self.configure(fg_color=THEME["bg"])
        ctk.set_appearance_mode("light")
    
    def _create_ui(self):
        """创建UI"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=35, pady=25)
        
        self._create_header(container)
        self._create_form(container)
        self._create_footer(container)
    
    def _create_header(self, parent):
        """创建头部"""
        # Logo
        try:
            img = ctk.CTkImage(
                Image.open(resource_path(CONFIG["logo_file"])), 
                size=CONFIG["logo_size"]
            )
            ctk.CTkLabel(parent, image=img, text="").pack(pady=(0, 10))
        except:
            pass
        
        # 标题
        ctk.CTkLabel(
            parent, 
            text=CONFIG["title"], 
            font=ctk.CTkFont(size=18, weight="bold"), 
            text_color=THEME["primary"]
        ).pack()
        
        ctk.CTkLabel(
            parent, 
            text=CONFIG["subtitle"], 
            font=ctk.CTkFont(size=13), 
            text_color=THEME["text_secondary"]
        ).pack(pady=(2, 15))
    
    def _create_form(self, parent):
        """创建表单"""
        card = ctk.CTkFrame(
            parent, 
            corner_radius=12, 
            fg_color=THEME["card_bg"], 
            border_width=1, 
            border_color=THEME["border"]
        )
        card.pack(fill="x", pady=5)
        
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(padx=25, pady=25)
        
        # 用户名
        self._create_field(form, "用户名", "请输入用户名")
        self.user_entry = self.last_entry
        
        # 密码
        self._create_field(form, "密码", "请输入密码", show="●")
        self.pass_entry = self.last_entry
        self.pass_entry.bind('<Return>', lambda e: self._handle_login())
        
        # 登录按钮
        self.login_btn = ctk.CTkButton(
            form, 
            text="登  录", 
            width=260, 
            height=42, 
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=THEME["primary"], 
            hover_color=THEME["primary_hover"],
            command=self._handle_login
        )
        self.login_btn.pack(pady=(15, 5))
        
        # 状态
        self.status = ctk.CTkLabel(form, text="", font=ctk.CTkFont(size=11))
        self.status.pack()
    
    def _create_field(self, parent, label, placeholder, show=None):
        """创建输入字段"""
        ctk.CTkLabel(
            parent, 
            text=label, 
            font=ctk.CTkFont(size=12), 
            text_color=THEME["text"], 
            anchor="w"
        ).pack(fill="x", pady=(0, 4))
        
        entry = ctk.CTkEntry(
            parent, 
            width=260, 
            height=40, 
            placeholder_text=placeholder,
            corner_radius=6, 
            border_color=THEME["border"], 
            font=ctk.CTkFont(size=12), 
            show=show
        )
        entry.pack(pady=(0, 12))
        self.last_entry = entry
    
    def _create_footer(self, parent):
        """创建页脚"""
        ctk.CTkLabel(
            parent, 
            text="© 2024 河南经济贸易技师学院", 
            font=ctk.CTkFont(size=10), 
            text_color=THEME["text_secondary"]
        ).pack(side="bottom", pady=5)
    
    def _handle_login(self):
        """处理登录"""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("提示", "请输入用户名和密码")
            return
        
        self.login_btn.configure(state="disabled", text="登录中...")
        self.status.configure(text="")
        
        def login_task():
            try:
                self.login_service.login(username, password)
                self._on_login_success()
            except Exception as e:
                self._on_login_error(str(e))
        
        threading.Thread(target=login_task, daemon=True).start()
    
    def _on_login_success(self):
        """登录成功回调"""
        self.status.configure(text="✓ 登录成功", text_color=THEME["success"])
        self.login_btn.configure(state="normal", text="登  录")
    
    def _on_login_error(self, error_msg):
        """登录失败回调"""
        self.login_btn.configure(state="normal", text="登  录")
        messagebox.showerror("错误", error_msg)
