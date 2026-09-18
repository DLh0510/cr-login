"""登录业务逻辑"""
from ..utils.browser import get_browser


class LoginService:
    """登录服务"""

    def __init__(self, login_url):
        self.login_url = login_url

    def login(self, username, password):
        """执行登录操作 - 打开AWS Skill Builder平台

        Args:
            username: 用户名（不进行验证）
            password: 密码（不进行验证）

        Raises:
            Exception: 浏览器启动失败时抛出异常
        """
        # 直接打开浏览器并导航到AWS Skill Builder（无需验证）
        driver = get_browser()
        driver.maximize_window()
        driver.get(self.login_url)
