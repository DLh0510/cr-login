# login_client.py
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import threading
import os
import sys

URL = "http://cloudraiser-admin-hnjm-471998617.us-east-1.elb.amazonaws.com/admin_login"

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

def login(username, password, btn, status_label):
    btn.configure(state='disabled', text='登录中...')
    try:
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
        driver.get(URL)
        driver.find_element(By.ID, "admin_user").send_keys(username)
        driver.find_element(By.ID, "admin_user_pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()
        status_label.configure(text="✓ 登录成功", text_color="#22c55e")
    except Exception as e:
        status_label.configure(text="")
        messagebox.showerror("错误", str(e))
    finally:
        btn.configure(state='normal', text='登  录')

def on_login():
    if not user_entry.get() or not pass_entry.get():
        messagebox.showwarning("提示", "请输入用户名和密码")
        return
    threading.Thread(target=login, args=(user_entry.get(), pass_entry.get(), login_btn, status_label), daemon=True).start()

# 设置主题
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# 主窗口
app = ctk.CTk()
app.title("河南经济贸易技师学院 - 云平台登录")
app.geometry("420x580")
app.resizable(False, False)

# 配色
PRIMARY_BLUE = "#1e6bb8"
DARK_BLUE = "#0d4a7c"

# 主容器
main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.pack(fill="both", expand=True, padx=40, pady=30)

# Logo
try:
    logo_img = ctk.CTkImage(Image.open(resource_path("yjgj_foot_logo.png")), size=(100, 100))
    logo_label = ctk.CTkLabel(main_frame, image=logo_img, text="")
    logo_label.pack(pady=(10, 5))
except:
    pass

# 标题
title_label = ctk.CTkLabel(main_frame, text="河南经济贸易技师学院", font=ctk.CTkFont(size=20, weight="bold"), text_color=PRIMARY_BLUE)
title_label.pack(pady=(5, 5))

subtitle_label = ctk.CTkLabel(main_frame, text="云平台管理系统", font=ctk.CTkFont(size=14), text_color="#666666")
subtitle_label.pack(pady=(0, 25))

# 登录卡片
card = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#ffffff", border_width=1, border_color="#e0e0e0")
card.pack(fill="x", pady=10, padx=5)

inner_frame = ctk.CTkFrame(card, fg_color="transparent")
inner_frame.pack(padx=30, pady=30)

# 用户名
user_label = ctk.CTkLabel(inner_frame, text="用户名", font=ctk.CTkFont(size=13), text_color="#333333", anchor="w")
user_label.pack(fill="x", pady=(0, 5))
user_entry = ctk.CTkEntry(inner_frame, width=280, height=42, placeholder_text="请输入用户名", corner_radius=8, border_color="#d0d0d0", font=ctk.CTkFont(size=13))
user_entry.pack(pady=(0, 15))

# 密码
pass_label = ctk.CTkLabel(inner_frame, text="密码", font=ctk.CTkFont(size=13), text_color="#333333", anchor="w")
pass_label.pack(fill="x", pady=(0, 5))
pass_entry = ctk.CTkEntry(inner_frame, width=280, height=42, placeholder_text="请输入密码", show="●", corner_radius=8, border_color="#d0d0d0", font=ctk.CTkFont(size=13))
pass_entry.pack(pady=(0, 20))
pass_entry.bind('<Return>', lambda e: on_login())

# 登录按钮
login_btn = ctk.CTkButton(inner_frame, text="登  录", width=280, height=45, corner_radius=8, 
                          font=ctk.CTkFont(size=15, weight="bold"), fg_color=PRIMARY_BLUE, 
                          hover_color=DARK_BLUE, command=on_login)
login_btn.pack(pady=(5, 10))

# 状态标签
status_label = ctk.CTkLabel(inner_frame, text="", font=ctk.CTkFont(size=12))
status_label.pack()

# 底部版权
footer = ctk.CTkLabel(main_frame, text="© 2024 河南经济贸易技师学院 版权所有", font=ctk.CTkFont(size=11), text_color="#999999")
footer.pack(side="bottom", pady=10)

app.mainloop()
