"""浏览器驱动管理"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


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
