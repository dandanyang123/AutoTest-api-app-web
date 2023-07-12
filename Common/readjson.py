import json
import os


# 读取接口数据
def read_api_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# 读取目录中的所有 JSON 文件
def get_all_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files