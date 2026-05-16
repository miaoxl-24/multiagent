import json
import os

def load_key(key_name: str):
    # 找到Keys.json文件的路径
    config_path = os.path.join(os.path.dirname(__file__), "Keys.json")
    # 读取文件
    with open(config_path, "r", encoding="utf-8") as f:
        keys = json.load(f)
    # 返回你要的key
    return keys.get(key_name)