import pytest
from PageObject.api.apitest import ApiTest
from config.conf import cm
from Common.readjson import get_all_json_files

# 执行所有单个接口测试用例
@pytest.mark.apismoke
def test_all_apis():
    json_files = get_all_json_files(cm.API_ELEMENT_PATH)
    for json_file in json_files:  # 遍历所有接口测试数据
        ApiTest().test_api(json_file)

