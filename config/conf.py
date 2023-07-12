import os
from selenium.webdriver.common.by import By
from utils.times import dt_strftime
 
class ConfigManager(object):
    # 项目目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # case 保存目录
    WEB_CASEPATH = os.path.join(BASE_DIR, 'TestCase/web')
    APP_CASEPATH = os.path.join(BASE_DIR, 'TestCase/app')
    API_CASEPATH = os.path.join(BASE_DIR, 'TestCase/api')
 
    # 页面元素目录
    WEB_ELEMENT_PATH = os.path.join(BASE_DIR, 'PageElement/web')
    APP_ELEMENT_PATH = os.path.join(BASE_DIR, 'PageElement/app')
    API_ELEMENT_PATH = os.path.join(BASE_DIR, 'PageElement/api')
 
    # 报告文件ELEMENT_PATH
    REPORT_FILE = os.path.join(BASE_DIR, 'Report/%s/report.html' % (dt_strftime("%Y%m%d%H%M%S")))
    # 元素定位的类型
    LOCATE_MODE = {
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'name': By.NAME,
        'id': By.ID,
        'class': By.CLASS_NAME
    }
 
    # 邮件信息
    EMAIL_INFO = {
        'username': 'q1343036903@163.com',  # 切换成你自己的地址
        'password': 'CFMMJDKJVCMGMKHV',
        'smtp_host': 'smtp.163.com',
        'smtp_port': 465
    }
 
    # 收件人
    ADDRESSEE = [
        'q1343036903@163.com',
    ]

    DRIVER_PATH = os.path.join(BASE_DIR, 'webdriver/chrome/chromedriver114.exe')
    DOWNLOAD_PATH = os.path.join(BASE_DIR, 'download_test')

    @property
    def log_file(self):
        """日志目录"""
        log_dir = os.path.join(self.BASE_DIR, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, '{}.log'.format(dt_strftime()))
 
    @property
    def ini_file(self):
        """配置文件"""
        ini_file = os.path.join(self.BASE_DIR, 'config', 'config.ini')
        if not os.path.exists(ini_file):
            raise FileNotFoundError("配置文件%s不存在！" % ini_file)
        return ini_file


 
 
cm = ConfigManager()
if __name__ == '__main__':
    print(cm.DRIVER_PATH)
