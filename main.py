import pytest
from config.conf import cm
from utils.send_mail import send_report


report = "--html=" + cm.REPORT_FILE  # 默认测试报告保存路径
case_path = cm.WEB_CASEPATH          # 默认测试用例路径

if __name__ == "__main__":
    mod = input("请指定运行平台(api/web/app)>>")
    if mod == "web" or mod == "":
        case_path = cm.WEB_CASEPATH
    elif mod == "app":
        case_path = cm.APP_CASEPATH
    else:
        case_path = cm.API_CASEPATH

    result = input("请输入运行模式(run or debug)>>")

    if result == "run":
        sendswitch = input("是否发送报告邮件(yes or no)>>")
        if sendswitch == "yes":
            send_report()
        pytest.main([report,
                     '-q',
                     '--capture=sys',
                     '--disable-pytest-warnings',
                     case_path
                     ])
    else:
        pytest.main([report,
                     '-sv',
                     '--capture=sys',
                     case_path
                     ])
