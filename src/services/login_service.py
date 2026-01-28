"""登录业务逻辑"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..utils.browser import get_browser


class LoginService:
    def __init__(self, login_url):
        self.login_url = login_url
    
    def login(self, username, password):
        driver = get_browser()
        driver.get(self.login_url)
        
        wait = WebDriverWait(driver, 10)
        
        # 等待并填写用户名
        user_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        user_input.clear()
        user_input.send_keys(username)
        
        # 填写密码
        pass_input = driver.find_element(By.ID, "password")
        pass_input.clear()
        pass_input.send_keys(password)
        
        # 点击登录按钮
        login_btn = driver.find_element(By.CSS_SELECTOR, "button.ant-btn-primary")
        login_btn.click()
