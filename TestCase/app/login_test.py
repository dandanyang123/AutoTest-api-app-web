from PageObject.app.loginpage import LoginPage as lp
import pytest

@pytest.mark.appsmoke
class TestLogin:

    def test_login(self):
        lp().login()
