# login_client.py
import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import threading

URL = "http://cloudraiser-admin-hnjm-471998617.us-east-1.elb.amazonaws.com/admin_login"

def login(username, password, btn):
    btn.config(state='disabled')
    try:
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
        driver.get(URL)
        driver.find_element(By.ID, "admin_user").send_keys(username)
        driver.find_element(By.ID, "admin_user_pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()
    except Exception as e:
        messagebox.showerror("错误", str(e))
    finally:
        btn.config(state='normal')

def on_login():
    threading.Thread(target=login, args=(user_entry.get(), pass_entry.get(), login_btn), daemon=True).start()

root = tk.Tk()
root.title("CloudRaiser Admin 登录")
root.geometry("280x160")
root.resizable(False, False)

ttk.Label(root, text="ID:").pack(pady=(15,5))
user_entry = ttk.Entry(root, width=30)
user_entry.pack()

ttk.Label(root, text="Password:").pack(pady=(10,5))
pass_entry = ttk.Entry(root, width=30, show="*")
pass_entry.pack()

login_btn = ttk.Button(root, text="Login", command=on_login)
login_btn.pack(pady=15)

root.mainloop()
