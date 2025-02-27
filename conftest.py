import pytest
from _pytest.config import Config
from playwright.sync_api import sync_playwright

from conf.bot import BotMsg
from conf.path_conf import cookies_path
from core.browser_manager import BrowserManager
from utils.json_loader import read_json
from utils.logger import Logger
from core.auth.login_state import LoginState

logger = Logger().get_logger()
log_obj = Logger()


@pytest.fixture(scope="session")
def get_browser_name(pytestconfig: Config):

    """获取 pytest 运行命令中指定要运行的浏览器名称，如果没有指定，则默认为 chromium"""

    return pytestconfig.getoption(name="--browser") or ["chromium"]


@pytest.fixture(scope="session")
def get_browser(get_browser_name):

    """初始化浏览器对象和浏览器对象单例"""

    with sync_playwright() as p:
        # 浏览器列表
        browser_list = {
            "chromium": p.chromium,
            "firefox": p.firefox,
            "webkit": p.webkit,
        }

        # 创建浏览器对象
        browser = browser_list.get(get_browser_name[0]).launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        # 初始化浏览器单例
        BrowserManager.initialize_browser(browser)

        yield browser
        browser.close()


@pytest.fixture(scope="session")
def get_browser_context(get_browser):

    """创建浏览器上下文对象并实现持久化登录"""

    browser_context = get_browser.new_context(locale="en")
    BrowserManager.initialize_context(browser_context)


    # 登录态检查
    LoginState.is_logged_in()
    # 等待登录完成，完成后给上下文对象添加登录态 cookies 数据
    browser_context.add_cookies(read_json(cookies_path))

    yield browser_context
    browser_context.close()


@pytest.fixture(scope="session", autouse=True)
def get_page(get_browser_context):

    """初始化页面对象和页面对象单例"""

    page = get_browser_context.new_page()
    BrowserManager.initialize_page(page)
    yield page
    page.close()


def pytest_runtest_makereport(item, call):

    """全局异常捕获"""

    if call.excinfo is not None:
        # 获取异常信息
        excinfo = call.excinfo
        # 获取异常发生的文件名、行号和错误消息
        filename = excinfo.traceback[-1].path
        lineno = excinfo.traceback[-1].lineno
        message = excinfo.value
        logger.error(f"测试用例 {item.name} 执行失败: {filename}:{lineno} - {message}")


def pytest_html_report_title(report):

    """设置测试报告标题"""
    report.title = f"{log_obj.get_current_date()} 第 {log_obj.get_current_round()} 批次测试报告"


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):

    """设置测试报告文件名称和保存路径"""

    report_name = f"report-{log_obj.get_the_datetime_of_the_log_name()}.html"
    report_path = log_obj.get_current_round_log_storage_path().joinpath(report_name)
    config.option.htmlpath = report_path


# 测试用例执行结果统计
test_stats = {
    'total': 0,        # 总测试用例数
    'passed': 0,       # 成功的测试用例数
    'failed': 0,       # 失败的测试用例数
    'skipped': 0       # 跳过的测试用例数
}

# 收集每个测试用例执行结果的钩子函数
def pytest_runtest_logreport(report):
    if report.when == 'call':
        test_stats['total'] += 1  # 总测试用例数加 1

        if report.outcome == 'passed':
            test_stats['passed'] += 1
        elif report.outcome == 'failed':
            test_stats['failed'] += 1
        elif report.outcome == 'skipped':
            test_stats['skipped'] += 1

# 计算并发送测试结果到飞书的钩子函数
def pytest_terminal_summary(terminalreporter):
    total = test_stats['total']
    passed = test_stats['passed']
    failed = test_stats['failed']
    skipped = test_stats['skipped']

    # 计算通过率和失败率
    pass_rate = (passed / total) * 100 if total > 0 else 0
    fail_rate = (failed / total) * 100 if total > 0 else 0

    # 构建群消息请求体
    message = {
        "post": {
            "zh_cn": {
                "title": "测试报告",
                "content": [
                    [{
                        "tag": "text",
                        "text": f""
                                f"用例总数: {total}"
                                f"通过数: {passed}"
                                f"失败数: {failed}"
                                f"跳过数: {skipped}"
                                f"----------------------"
                                f"通过率: {pass_rate}%"
                                f"失败率: {fail_rate}%"
                    }, {
                        "tag": "a",
                        "text": "测试报告",
                        "href": "http://www.example.com/"
                    }]
                ]
            }
        }
    }

    # 发送消息到飞书或其他办公工具
    BotMsg.test_result_notify(message)
