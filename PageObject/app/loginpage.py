from Common.BaseApp import BaseApp
from Common.readappelement import Element

class LoginPage(BaseApp):
    def login(self):
        self.el = Element("login_page")
        self.click_on_element(*self.el["首页应用合集"])
        self.click_on_element(*self.el["设置"])
        self.click_on_element(*self.el["点击wifi"])
