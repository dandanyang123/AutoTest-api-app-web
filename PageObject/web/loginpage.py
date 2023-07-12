from Common.BasePage import BasePage
from Common.readconfig import ini
from Common.readwebelement import Element

class LoginPage(BasePage):

    el: Element

    def login(self, username, password):
        self.el = Element("login_page")
        self.load_url(ini.url)
        self.send_keys(*self.el["登录账号框"], username)
        self.send_keys(*self.el["登录密码框"], password)
        self.click(*self.el["登陆确认按钮"])
