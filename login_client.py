# login_client.py
"""提示词工程课程实训平台 - 登录客户端"""
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import threading
import os
import sys

# ============ 配置 ============
CONFIG = {
    "url": "https://skillbuilder.aws/",
    "title": "提示词工程课程实训平台",
    "subtitle": "Prompt Engineering Practice Platform",
    "window_size": "480x650",
    "logo_size": (80, 80),
}

# ============ 主题 ============
THEME = {
    "primary": "#7c3aed",      # 紫色主题，适合AI/提示词工程
    "primary_hover": "#6d28d9",
    "bg": "#0f0a1e",           # 深紫黑背景
    "card_bg": "#1a1232",
    "text": "#f3f0ff",
    "text_secondary": "#a78bfa",
    "border": "#5b21b6",
    "success": "#10b981",
    "error": "#ef4444",
}

# ============ 工具函数 ============
def resource_path(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    return os.path.join(base, path)

def get_browser():
    """尝试获取可用的浏览器驱动"""
    errors = []

    # 尝试 Chrome
    try:
        print("正在尝试启动 Chrome (webdriver_manager)...")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        print("Chrome 启动成功！")
        return driver
    except Exception as e:
        error_msg = f"Chrome (webdriver_manager) 失败: {str(e)}"
        print(error_msg)
        errors.append(error_msg)

    # 尝试 Edge
    try:
        print("正在尝试启动 Edge (webdriver_manager)...")
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        print("Edge 启动成功！")
        return driver
    except Exception as e:
        error_msg = f"Edge (webdriver_manager) 失败: {str(e)}"
        print(error_msg)
        errors.append(error_msg)

    # 尝试系统默认 Chrome
    try:
        print("正在尝试启动系统默认 Chrome...")
        driver = webdriver.Chrome()
        print("系统默认 Chrome 启动成功！")
        return driver
    except Exception as e:
        error_msg = f"系统默认 Chrome 失败: {str(e)}"
        print(error_msg)
        errors.append(error_msg)

    # 尝试系统默认 Edge
    try:
        print("正在尝试启动系统默认 Edge...")
        driver = webdriver.Edge()
        print("系统默认 Edge 启动成功！")
        return driver
    except Exception as e:
        error_msg = f"系统默认 Edge 失败: {str(e)}"
        print(error_msg)
        errors.append(error_msg)

    # 所有方法都失败了
    error_summary = "\n".join(errors)
    raise Exception(f"无法启动浏览器！请确保已安装 Chrome 或 Edge 浏览器。\n\n详细错误：\n{error_summary}")

# ============ 登录逻辑 ============
class LoginService:
    @staticmethod
    def login(username, password, on_success, on_error):
        try:
            # 直接打开浏览器，无需验证账号密码
            driver = get_browser()
            driver.maximize_window()
            driver.get(CONFIG["url"])
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
        self.title(CONFIG['title'])
        self.geometry(CONFIG["window_size"])
        self.resizable(False, False)
        self.configure(fg_color=THEME["bg"])
        ctk.set_appearance_mode("dark")
    
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
        except:
            ctk.CTkLabel(parent, text="🤖", font=ctk.CTkFont(size=50)).pack(pady=(5, 10))

        # 标题
        ctk.CTkLabel(parent, text=CONFIG["title"], font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=THEME["text_secondary"]).pack()
        ctk.CTkLabel(parent, text=CONFIG["subtitle"], font=ctk.CTkFont(size=12),
                     text_color=THEME["primary"]).pack(pady=(2, 15))
    
    def _create_form(self, parent):
        # 卡片
        card = ctk.CTkFrame(parent, corner_radius=12, fg_color=THEME["card_bg"], 
                           border_width=1, border_color=THEME["border"])
        card.pack(fill="x", pady=5)
        
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(padx=25, pady=25)
        
        # 用户名
        self._create_field(form, "学员账号", "请输入学员账号")
        self.user_entry = self.last_entry

        # 密码
        self._create_field(form, "登录密码", "请输入登录密码", show="●")
        self.pass_entry = self.last_entry
        self.pass_entry.bind('<Return>', lambda e: self._on_login())

        # 登录按钮
        self.login_btn = ctk.CTkButton(form, text="🚀 进入课程平台", width=260, height=45, corner_radius=8,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       fg_color=THEME["primary"], hover_color=THEME["primary_hover"],
                                       text_color="#ffffff",
                                       command=self._on_login)
        self.login_btn.pack(pady=(15, 5))

        # 状态
        self.status = ctk.CTkLabel(form, text="", font=ctk.CTkFont(size=11), text_color=THEME["text_secondary"])
        self.status.pack()
    
    def _create_field(self, parent, label, placeholder, show=None):
        ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=12),
                     text_color=THEME["text_secondary"], anchor="w").pack(fill="x", pady=(0, 4))
        entry = ctk.CTkEntry(parent, width=260, height=40, placeholder_text=placeholder,
                            corner_radius=8, border_color=THEME["border"],
                            fg_color=THEME["card_bg"], text_color=THEME["text"],
                            font=ctk.CTkFont(size=12), show=show)
        entry.pack(pady=(0, 12))
        self.last_entry = entry
    
    def _create_footer(self, parent):
        ctk.CTkLabel(parent, text="© 2024 提示词工程课程实训平台 | AWS Skill Builder",
                     font=ctk.CTkFont(size=9), text_color=THEME["text_secondary"]).pack(side="bottom", pady=5)
    
    def _on_login(self):
        username, password = self.user_entry.get().strip(), self.pass_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("⚠ 提示", "请输入学员账号和密码")
            return

        self.login_btn.configure(state="disabled", text="🔄 正在登录...")
        self.status.configure(text="正在打开课程平台...", text_color=THEME["text_secondary"])

        def on_success():
            self.status.configure(text="✓ 登录成功！", text_color=THEME["success"])
            self.login_btn.configure(state="normal", text="🚀 进入课程平台")

        def on_error(msg):
            self.login_btn.configure(state="normal", text="🚀 进入课程平台")
            self.status.configure(text="")
            messagebox.showerror("✖ 登录失败", msg)

        threading.Thread(target=LoginService.login, args=(username, password, on_success, on_error), daemon=True).start()

# ============ 入口 ============
if __name__ == "__main__":
    LoginApp().mainloop()
