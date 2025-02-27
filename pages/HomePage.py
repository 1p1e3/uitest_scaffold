"""
运用 Page Object 页面对象模型构建具体的页面类
Use the Page Object Model (POM) to construct specific page classes.
"""
from core.base_page import BasePage


class HomePage(BasePage):
    def __init__(self):
        super().__init__()
        """
        初始化当前页面中的元素定位器
        """

    def operation_a(self):
        """
        当前页面上的某个操作。
        在此方法中调用 init 方法中的定位器，再调用需要的元素操作方法，完成页面上的这个功能操作
        """
        pass

    def operation_b(self):
        pass