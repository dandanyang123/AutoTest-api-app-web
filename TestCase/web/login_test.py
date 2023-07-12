from PageObject.web.loginpage import LoginPage as lp
import pytest
from Common.readwebelement import Element
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.mark.websmoke
class TestLogin:

    def test_login(self):
        self.el = Element("login_page")
        lp().login(username=self.el['登录账号'][1], password=self.el['登录密码'][1])