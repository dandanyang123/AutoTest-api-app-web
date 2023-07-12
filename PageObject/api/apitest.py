from Common.BaseApi import APIClient
from Common.readjson import read_api_data, get_all_json_files


class ApiTest(APIClient):

    def test_api(self, endpoint):
        # 读取接口数据
        api_data = read_api_data(endpoint)

        # 遍历接口数据
        for api in api_data:
            # 提取接口信息
            name = api['name']
            url = api['url']
            method = api['method']
            headers = api['headers']
            params = api.get('params')
            expected_status = api['expected_status']
            expected_response = api['expected_response']

            # 发送接口请求
            if method == "GET":

                response = self.get(url, params=params, headers=headers)
            elif method == "POST":
                response = self.post(url, data=params, headers=headers)
            else:
                raise(f"Unsupported HTTP method: {method}")

            # 断言状态码
            assert response.status_code == expected_status

            # 断言响应数据
            assert response.json() == expected_response