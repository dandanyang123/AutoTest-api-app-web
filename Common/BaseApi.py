import requests

class APIClient(object):
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, url, params=None, headers=None):
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()  # 检查响应状态码，如果不是 2xx，抛出异常
            return response
        except requests.RequestException as e:
            print(f"请求发生异常: {e}")
            raise

    def post(self, url, data=None, headers=None):
        try:
            response = self.session.post(url, json=data, headers=headers, timeout=self.timeout)
            response.raise_for_status()  # 检查响应状态码，如果不是 2xx，抛出异常
            return response
        except requests.RequestException as e:
            print(f"请求发生异常: {e}")
            raise
# url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
# url = "https://fanyi-api.baidu.com/api/trans/vip/translate?q=test&from=en&to=zh&appid=20210103000662374&salt=555&sign=6920f89156766aece32ac15afcd6ff3b"
#
# params = {
#     "q": "test",
#     "from": "en",
#     "to": "zh",
#     "appid": "20210103000662374",
#     "salt": "1435660288",
#     "sign": "6920f89156766aece32ac15afcd6ff3b"
# }
#
# p = APIClient()
# print(p.get(url).text)