# login_client.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import threading
import os
import sys

URL = "http://cloudraiser-admin-hnjm-471998617.us-east-1.elb.amazonaws.com/admin_login"

# 获取资源路径
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

def login(username, password, btn, status_label):
    btn.config(state='disabled')
    status_label.config(text="正在登录...")
    try:
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
        driver.get(URL)
        driver.find_element(By.ID, "admin_user").send_keys(username)
        driver.find_element(By.ID, "admin_user_pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()
        status_label.config(text="登录成功")
    except Exception as e:
        status_label.config(text="")
        messagebox.showerror("错误", str(e))
    finally:
        btn.config(state='normal')

def on_login():
    if not user_entry.get() or not pass_entry.get():
        messagebox.showwarning("提示", "请输入用户名和密码")
        return
    threading.Thread(target=login, args=(user_entry.get(), pass_entry.get(), login_btn, status_label), daemon=True).start()

def on_enter(event):
    on_login()

# 主窗口
root = tk.Tk()
root.title("河南经济贸易技师学院 - 云平台登录")
root.geometry("480x580")
root.resizable(False, False)
root.configure(bg='#f5f7fa')

# 配色
PRIMARY_BLUE = '#1e6bb8'
LIGHT_BLUE = '#e8f4fc'
DARK_BLUE = '#0d4a7c'
WHITE = '#ffffff'
GRAY = '#666666'

# 顶部蓝色条
header = tk.Frame(root, bg=PRIMARY_BLUE, height=80)
header.pack(fill='x')
header.pack_propagate(False)

title_label = tk.Label(header, text="河南经济贸易技师学院", font=('PingFang SC', 18, 'bold'), fg=WHITE, bg=PRIMARY_BLUE)
title_label.pack(pady=25)

# Logo
logo_frame = tk.Frame(root, bg='#f5f7fa')
logo_frame.pack(pady=20)

try:
    logo_img = Image.open(resource_path("yjgj_foot_logo.png"))
    logo_img = logo_img.resize((120, 120), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(logo_frame, image=logo_photo, bg='#f5f7fa')
    logo_label.image = logo_photo
    logo_label.pack()
except:
    pass

# 登录卡片
card = tk.Frame(root, bg=WHITE, padx=40, pady=30)
card.pack(pady=10)

login_title = tk.Label(card, text="云平台管理系统", font=('PingFang SC', 16, 'bold'), fg=DARK_BLUE, bg=WHITE)
login_title.pack(pady=(0, 20))

# 用户名
user_frame = tk.Frame(card, bg=WHITE)
user_frame.pack(fill='x', pady=8)
tk.Label(user_frame, text="用户名", font=('PingFang SC', 11), fg=GRAY, bg=WHITE, anchor='w').pack(fill='x')
user_entry = tk.Entry(user_frame, font=('PingFang SC', 12), width=28, relief='solid', bd=1)
user_entry.pack(fill='x', ipady=8, pady=(5,0))
user_entry.configure(highlightthickness=2, highlightcolor=PRIMARY_BLUE)

# 密码
pass_frame = tk.Frame(card, bg=WHITE)
pass_frame.pack(fill='x', pady=8)
tk.Label(pass_frame, text="密码", font=('PingFang SC', 11), fg=GRAY, bg=WHITE, anchor='w').pack(fill='x')
pass_entry = tk.Entry(pass_frame, font=('PingFang SC', 12), width=28, show="●", relief='solid', bd=1)
pass_entry.pack(fill='x', ipady=8, pady=(5,0))
pass_entry.configure(highlightthickness=2, highlightcolor=PRIMARY_BLUE)
pass_entry.bind('<Return>', on_enter)

# 登录按钮
login_btn = tk.Button(card, text="登 录", font=('PingFang SC', 14, 'bold'), fg=WHITE, bg=PRIMARY_BLUE,
                      activebackground=DARK_BLUE, activeforeground=WHITE, relief='flat', cursor='hand2',
                      width=20, height=2, command=on_login)
login_btn.pack(pady=(20, 10))

# 状态标签
status_label = tk.Label(card, text="", font=('PingFang SC', 9), fg=PRIMARY_BLUE, bg=WHITE)
status_label.pack()

# 底部版权
footer = tk.Label(root, text="© 2024 河南经济贸易技师学院 版权所有", font=('PingFang SC', 9), fg=GRAY, bg='#f5f7fa')
footer.pack(side='bottom', pady=15)

root.mainloop()
