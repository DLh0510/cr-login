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
        self.title(f"{CONFIG['title']} - {CONFIG['subtitle']}")
        self.geometry("480x650")
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
        self._create_form(content)
        self._create_log_panel(content)
        self._create_footer(content)
    
    def _create_header(self, parent):
        try:
            img = ctk.CTkImage(Image.open(resource_path(CONFIG["logo_file"])), size=(70, 70))
            ctk.CTkLabel(parent, image=img, text="").pack(pady=(5, 10))
        except:
            ctk.CTkLabel(parent, text="🛡️", font=ctk.CTkFont(size=50)).pack(pady=(5, 10))
        
        ctk.CTkLabel(parent, text=CONFIG["title"], font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#00d4ff").pack(pady=(5, 0))
        ctk.CTkLabel(parent, text=CONFIG["subtitle"].upper(), font=ctk.CTkFont(family="Courier", size=11),
                     text_color="#4a9eff").pack(pady=(2, 15))
    
    def _create_form(self, parent):
        form = ctk.CTkFrame(parent, fg_color="transparent")
        form.pack(fill="x", pady=5)
        
        self.user_entry = self._create_input(form, "OPERATOR ID / 参赛账号", "user")
        self.pass_entry = self._create_input(form, "ACCESS KEY / 安全密钥", "pass", show="●")
        
        opt_frame = ctk.CTkFrame(form, fg_color="transparent")
        opt_frame.pack(fill="x", pady=(5, 15))
        ctk.CTkCheckBox(opt_frame, text="保持安全连接", font=ctk.CTkFont(size=11),
                        text_color="#4a9eff", fg_color="#00d4ff", border_color="#1e3a5f").pack(side="left")
        ctk.CTkLabel(opt_frame, text="密钥重置", font=ctk.CTkFont(size=11), text_color="#4a9eff", cursor="hand2").pack(side="right")
        
        self.login_btn = ctk.CTkButton(form, text="⟳  初始化会话 / LOGIN", height=50, corner_radius=4,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       fg_color="#00d4ff", hover_color="#00a8cc", text_color="#0a0e14",
                                       command=self._handle_login)
        self.login_btn.pack(fill="x", pady=(5, 0))
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
        
        icon = "👤" if name == "user" else "👁"
        ctk.CTkLabel(inner, text=icon, font=ctk.CTkFont(size=16), text_color="#3d5a80").pack(side="right")
        return entry
    
    def _create_log_panel(self, parent):
        ctk.CTkFrame(parent, height=1, fg_color="#1e3a5f").pack(fill="x", pady=(15, 10))
        ctk.CTkLabel(parent, text="SYSTEM LOG:", font=ctk.CTkFont(family="Courier", size=11),
                     text_color="#4a9eff", anchor="w").pack(fill="x")
        
        self.log_frame = ctk.CTkFrame(parent, fg_color="transparent", height=100)
        self.log_frame.pack(fill="x", pady=(5, 0))
        self.log_frame.pack_propagate(False)
        
        self.log_labels = []
        logs = ["> 握手协议已建立", "> 正在连接安全服务器...", "> 系统完整性检查通过",
                "> 等待用户凭证...", "> 加密通道已启用 (AES-256)"]
        for log in logs:
            lbl = ctk.CTkLabel(self.log_frame, text=log, font=ctk.CTkFont(family="Courier", size=10),
                              text_color="#00ff88", anchor="w")
            lbl.pack(fill="x")
            self.log_labels.append(lbl)
    
    def _create_footer(self, parent):
        ctk.CTkFrame(parent, height=1, fg_color="#1e3a5f").pack(fill="x", pady=(15, 8))
        ctk.CTkLabel(parent, text="SECURE CONNECTION | TLS v1.3 ENCRYPTED",
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
            messagebox.showwarning("⚠ ALERT", "请输入账号和密钥")
            return
        
        self.login_btn.configure(state="disabled", text="⟳  正在初始化...")
        self._add_log("> 正在验证凭证...")
        
        def login_task():
            try:
                self.login_service.login(username, password)
                self.after(0, self._on_success)
            except Exception as e:
                self.after(0, lambda: self._on_error(str(e)))
        
        threading.Thread(target=login_task, daemon=True).start()
    
    def _on_success(self):
        self._add_log("> ✓ 会话初始化成功")
        self.login_btn.configure(state="normal", text="⟳  初始化会话 / LOGIN")
    
    def _on_error(self, msg):
        self._add_log(f"> ✖ 错误: {msg[:30]}")
        self.login_btn.configure(state="normal", text="⟳  初始化会话 / LOGIN")
        messagebox.showerror("✖ CONNECTION FAILED", msg)
