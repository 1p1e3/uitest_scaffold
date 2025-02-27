"""
实现持久化登录，这里以 google 登录为例
Implement persistent login using Google login as an example.
"""

from pathlib import Path
from conf.path_conf import cookies_path
from core.browser_manager import BrowserManager
from utils.json_loader import save_as_json
from utils.logger import Logger

logger = Logger().get_logger()


class LoginState:

    @classmethod
    def google_login(cls):

        """谷歌登录"""

        # 获取浏览器相关实例(单例)
        cls.browser = BrowserManager.get_browser()
        cls.context = cls.browser.new_context()
        cls.page = cls.context.new_page()


        # 点击 Google 登录按钮之后等待出现谷歌登录弹窗
        with cls.context.expect_page() as new_page_info:
            cls.page.locator("button").filter(has_text="Google").click()
        # popup_page 为谷歌登录弹窗对象
        popup_page = new_page_info.value
        popup_page.wait_for_load_state()

        # 定位元素，输入账密
        popup_page.wait_for_selector("input[type='email']", state="visible")
        popup_page.fill("input[type='email']", "")
        popup_page.click("#identifierNext")

        popup_page.wait_for_selector("input[type='password']", state="visible")
        popup_page.fill("input[type='password']", "")
        popup_page.click("#passwordNext")

        # 登录之后一般会有一个跳转到首页的过程
        # 等待跳转到首页
        cls.page.wait_for_url("", wait_until="domcontentloaded", timeout=50000)

        # 跳转到首页，且页面也加载完成之后，此时的 cookies 才是有效的
        # 此时保存登录之后的所有 cookie 数据
        cookies = cls.context.cookies()
        save_as_json(path=cookies_path, content=cookies, name="cookies")

        # 关闭页面、上下文、浏览器
        cls.page.close()
        cls.context.close()
        cls.browser.close()


    @classmethod
    def re_login(cls):

        """重新登录"""

        re_login_times = 0
        while not cls.is_cookies_json_exists():
            re_login_times += 1
            logger.info(f"重新登录, 次数: {re_login_times}")
            cls.google_login()


    @classmethod
    def is_cookies_json_exists(cls):

        """判断 cookies json 是否保存成功"""

        if not Path(cookies_path).exists():
            logger.info("cookies json 不存在")
            return False
        else:
            logger.info("cookies json 存在")
            return True


    @classmethod
    def is_logged_in(cls):

        """登录/未登录状态处理"""

        if not cls.is_cookies_json_exists():
            logger.info("cookies json 不存在，可能未登录，开始重新登录")
            cls.re_login()
        else:
            """
            实际场景中登录态可能会存在失效、或者登录态有效时间太短，很快就会过期等情况
            可以进一步拓展
            """
            logger.info("cookies json 存在，目前是登录状态")