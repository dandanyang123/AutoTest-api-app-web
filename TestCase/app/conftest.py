import pytest
import uiautomator2 as u2
from Common.readconfig import ini
from Script.inspect import inspect_element
import os


def init_device():
    while 1:
        try:
            os.system('python -m uiautomator2 init')
            break
        except u2.adbutils.AdbError:
            print("初始化设备失败！重启adb")
            os.system('adb kill-server && adb start-server')
            continue


init_device()
driver = u2.connect(ini.device_name)


@pytest.fixture(scope='session', autouse=True)
def drivers(request):
    """
    :param request: python内置的fixture函数，本函数中用来注册终结函数
    :return: 返回driver实例
    """
    global driver
    inspect_element()  # 元素检查
    driver.unlock()
    driver.press('home')

    def fn():
        print("quit")

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
    """
    截图保存为base64
    :return:
    """
    return driver.screenshot()
