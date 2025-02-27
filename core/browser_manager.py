"""
浏览器管理器单例类
负责管理整个测试框架的浏览器生命周期

Browser manager singleton class
Responsible for managing the browser lifecycle of the entire testing framework.
"""
from playwright.sync_api import Page, Browser, BrowserContext


class BrowserManager:
    # 实例对象
    instance = None
    # 页面实例
    page = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(BrowserManager, cls).__new__(cls)
        return cls.instance

    @classmethod
    def initialize_page(cls, page):
        """初始化页面实例"""
        cls.page = page

    @classmethod
    def initialize_browser(cls, browser):
        """初始化驱动实例"""
        cls.browser = browser

    @classmethod
    def initialize_context(cls, context):
        """初始化上下文实例"""
        cls.context = context

    @classmethod
    def get_browser(cls) -> Browser:
        """获取浏览器实例"""
        if not cls.browser:
            raise RuntimeError("获取浏览器实例失败")
        return cls.browser

    @classmethod
    def get_context(cls) -> BrowserContext:
        """获取上下文实例"""
        if not cls.context:
            raise RuntimeError("获取上下文实例失败")
        return cls.context

    @classmethod
    def get_page(cls) -> Page:
        """获取页面实例"""
        if not cls.page:
            raise RuntimeError("获取页面实例失败")
        return cls.page