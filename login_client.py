# login_client.py
"""河南经济贸易技师学院 - 云平台登录客户端"""
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import threading
import os
import sys

# ============ 配置 ============
CONFIG = {
    "url": "http://cloudraiser-admin-hnjm-471998617.us-east-1.elb.amazonaws.com/admin_login",
    "title": "河南经济贸易技师学院",
    "subtitle": "云平台管理系统",
    "window_size": "400x520",
    "logo_size": (90, 90),
}

# ============ 主题 ============
THEME = {
    "primary": "#1e6bb8",
    "primary_hover": "#155a9c",
    "bg": "#f0f4f8",
    "card_bg": "#ffffff",
    "text": "#1a1a2e",
    "text_secondary": "#64748b",
    "border": "#e2e8f0",
    "success": "#22c55e",
    "error": "#ef4444",
}

# ============ 工具函数 ============
def resource_path(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    return os.path.join(base, path)

def get_browser():
    """尝试获取可用的浏览器驱动"""
    # 尝试 Chrome
    try:
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    except:
        pass
    
    # 尝试 Edge
    try:
        return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    except:
        pass
    
    # 尝试系统默认 Chrome
    try:
        return webdriver.Chrome()
    except:
        pass
    
    # 尝试系统默认 Edge
    try:
        return webdriver.Edge()
    except:
        pass
    
    raise Exception("无法启动浏览器，请确保已安装 Chrome 或 Edge 浏览器")

# ============ 登录逻辑 ============
class LoginService:
    @staticmethod
    def login(username, password, on_success, on_error):
        try:
            driver = get_browser()
            driver.get(CONFIG["url"])
            driver.find_element(By.ID, "admin_user").send_keys(username)
            driver.find_element(By.ID, "admin_user_pass").send_keys(password)
            driver.find_element(By.NAME, "login").click()
            on_success()
        except Exception as e:
            on_error(str(e))

# ============ UI 组件 ============
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._create_ui()
    
    def _setup_window(self):
        self.title(f"{CONFIG['title']} - {CONFIG['subtitle']}")
        self.geometry(CONFIG["window_size"])
        self.resizable(False, False)
        self.configure(fg_color=THEME["bg"])
        ctk.set_appearance_mode("light")
    
    def _create_ui(self):
        # 主容器
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=35, pady=25)
        
        self._create_header(container)
        self._create_form(container)
        self._create_footer(container)
    
    def _create_header(self, parent):
        # Logo
        try:
            img = ctk.CTkImage(Image.open(resource_path("yjgj_foot_logo.png")), size=CONFIG["logo_size"])
            ctk.CTkLabel(parent, image=img, text="").pack(pady=(0, 10))
        except: pass
        
        # 标题
        ctk.CTkLabel(parent, text=CONFIG["title"], font=ctk.CTkFont(size=18, weight="bold"), 
                     text_color=THEME["primary"]).pack()
        ctk.CTkLabel(parent, text=CONFIG["subtitle"], font=ctk.CTkFont(size=13), 
                     text_color=THEME["text_secondary"]).pack(pady=(2, 15))
    
    def _create_form(self, parent):
        # 卡片
        card = ctk.CTkFrame(parent, corner_radius=12, fg_color=THEME["card_bg"], 
                           border_width=1, border_color=THEME["border"])
        card.pack(fill="x", pady=5)
        
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(padx=25, pady=25)
        
        # 用户名
        self._create_field(form, "用户名", "请输入用户名")
        self.user_entry = self.last_entry
        
        # 密码
        self._create_field(form, "密码", "请输入密码", show="●")
        self.pass_entry = self.last_entry
        self.pass_entry.bind('<Return>', lambda e: self._on_login())
        
        # 登录按钮
        self.login_btn = ctk.CTkButton(form, text="登  录", width=260, height=42, corner_radius=8,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       fg_color=THEME["primary"], hover_color=THEME["primary_hover"],
                                       command=self._on_login)
        self.login_btn.pack(pady=(15, 5))
        
        # 状态
        self.status = ctk.CTkLabel(form, text="", font=ctk.CTkFont(size=11))
        self.status.pack()
    
    def _create_field(self, parent, label, placeholder, show=None):
        ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=12), 
                     text_color=THEME["text"], anchor="w").pack(fill="x", pady=(0, 4))
        entry = ctk.CTkEntry(parent, width=260, height=40, placeholder_text=placeholder,
                            corner_radius=6, border_color=THEME["border"], 
                            font=ctk.CTkFont(size=12), show=show)
        entry.pack(pady=(0, 12))
        self.last_entry = entry
    
    def _create_footer(self, parent):
        ctk.CTkLabel(parent, text="© 2024 河南经济贸易技师学院", 
                     font=ctk.CTkFont(size=10), text_color=THEME["text_secondary"]).pack(side="bottom", pady=5)
    
    def _on_login(self):
        username, password = self.user_entry.get().strip(), self.pass_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("提示", "请输入用户名和密码")
            return
        
        self.login_btn.configure(state="disabled", text="登录中...")
        self.status.configure(text="")
        
        def on_success():
            self.status.configure(text="✓ 登录成功", text_color=THEME["success"])
            self.login_btn.configure(state="normal", text="登  录")
        
        def on_error(msg):
            self.login_btn.configure(state="normal", text="登  录")
            messagebox.showerror("错误", msg)
        
        threading.Thread(target=LoginService.login, args=(username, password, on_success, on_error), daemon=True).start()

# ============ 入口 ============
if __name__ == "__main__":
    LoginApp().mainloop()
