
import pytest
from py.xml import html
from selenium import webdriver
from config.conf import cm
from Script.inspect import inspect_element

chromeOptions = webdriver.ChromeOptions()
# 忽略证书认证/ssl错误和无用日志
chromeOptions.add_argument('--ignore-certificate-errors')
chromeOptions.add_argument('--ignore-ssl-errors')
chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
# chromeOptions.add_argument("--headless")

prefs = {
    "download.default_directory": cm.DOWNLOAD_PATH,
    "profile.default_content_setting_values.automatic_downloads": False,
    'download.prompt_for_download': False,  # 是否弹出下载页
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False
}

chromeOptions.add_argument('lang=zh_CN.utf-8')  # 反爬虫
chromeOptions.add_experimental_option("prefs", prefs)
chromeOptions.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=chromeOptions, executable_path=cm.DRIVER_PATH)



@pytest.fixture(scope='session', autouse=True)
def drivers(request):
    """

    :param request: python内置的fixture函数，本函数中用来注册终结函数
    :return: 返回driver实例
    """
    global driver
    driver.maximize_window()
    inspect_element()  # 元素检查
    def fn():
        driver.quit()

    request.addfinalizer(fn)
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:1024px;height:768px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


# def pytest_html_results_table_header(cells):
#     cells.insert(1, html.th('用例名称'))
#     cells.insert(2, html.th('Test_nodeid'))
#     cells.pop(2)
#
#
# def pytest_html_results_table_row(report, cells):
#     cells.insert(1, html.td(report.description))
#     cells.insert(2, html.td(report.nodeid))
#     cells.pop(2)
#
#
# def pytest_html_results_table_html(report, data):
#     if report.passed:
#         del data[:]
#         data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))


def _capture_screenshot():
    '''
    截图保存为base64
    :return:
    '''
    return driver.get_screenshot_as_base64()


