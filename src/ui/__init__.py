"""UI模块"""

def __getattr__(name):
    """延迟导入，避免在导入模块时就加载 tkinter"""
    if name == "LoginWindow":
        from .login_window import LoginWindow
        return LoginWindow
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = ['LoginWindow']
