"""浏览器驱动管理"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_browser():
    """尝试获取可用的浏览器驱动"""
    errors = []

    # 尝试 Chrome (使用 webdriver_manager)
    try:
        logger.info("正在尝试启动 Chrome (webdriver_manager)...")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        logger.info("Chrome 启动成功！")
        return driver
    except Exception as e:
        error_msg = f"Chrome (webdriver_manager) 失败: {str(e)}"
        logger.warning(error_msg)
        errors.append(error_msg)

    # 尝试 Edge (使用 webdriver_manager)
    try:
        logger.info("正在尝试启动 Edge (webdriver_manager)...")
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        logger.info("Edge 启动成功！")
        return driver
    except Exception as e:
        error_msg = f"Edge (webdriver_manager) 失败: {str(e)}"
        logger.warning(error_msg)
        errors.append(error_msg)

    # 尝试系统默认 Chrome
    try:
        logger.info("正在尝试启动系统默认 Chrome...")
        driver = webdriver.Chrome()
        logger.info("系统默认 Chrome 启动成功！")
        return driver
    except Exception as e:
        error_msg = f"系统默认 Chrome 失败: {str(e)}"
        logger.warning(error_msg)
        errors.append(error_msg)

    # 尝试系统默认 Edge
    try:
        logger.info("正在尝试启动系统默认 Edge...")
        driver = webdriver.Edge()
        logger.info("系统默认 Edge 启动成功！")
        return driver
    except Exception as e:
        error_msg = f"系统默认 Edge 失败: {str(e)}"
        logger.warning(error_msg)
        errors.append(error_msg)

    # 所有方法都失败了
    error_summary = "\n".join(errors)
    raise Exception(f"无法启动浏览器！请确保已安装 Chrome 或 Edge 浏览器。\n\n详细错误：\n{error_summary}")
