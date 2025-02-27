"""
对应页面类下的测试用例
Test cases under the corresponding page class.
"""
from pages.HomePage import HomePage


class TestHomePage:
    def test_case1(self):
        HomePage().operation_a()
        HomePage().operation_b()
        """后续再进行断言"""