"""登录业务逻辑"""
from selenium.webdriver.common.by import By
from ..utils.browser import get_browser


class LoginService:
    """登录服务"""
    
    def __init__(self, login_url):
        self.login_url = login_url
    
    def login(self, username, password):
        """执行登录操作
        
        Args:
            username: 用户名
            password: 密码
            
        Raises:
            Exception: 登录失败时抛出异常
        """
        driver = get_browser()
        driver.get(self.login_url)
        driver.find_element(By.ID, "admin_user").send_keys(username)
        driver.find_element(By.ID, "admin_user_pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()
