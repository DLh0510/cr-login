"""登录业务逻辑"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..utils.browser import get_browser


class LoginService:
    def __init__(self, login_url):
        self.login_url = login_url
    
    def login(self, event_code, user_id, password, player_name):
        driver = get_browser()
        driver.get(self.login_url)
        
        wait = WebDriverWait(driver, 10)
        
        # EventCode
        wait.until(EC.presence_of_element_located((By.ID, "event_id"))).send_keys(event_code)
        # ID
        driver.find_element(By.ID, "lab_user").send_keys(user_id)
        # Password
        driver.find_element(By.ID, "lab_user_pass").send_keys(password)
        # Player Name
        driver.find_element(By.ID, "lab_user_name").send_keys(player_name)
        # Login
        driver.find_element(By.CSS_SELECTOR, "button").click()
