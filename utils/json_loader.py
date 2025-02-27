"""
json 文件操作
Operations related to JSON files.
"""

import json
from utils.logger import Logger

logger = Logger().get_logger()

def save_as_json(path: str, content, name):

    """保存为 json"""

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj=content, fp=f, ensure_ascii=False, indent=4)
            logger.info(f"{name} 数据: {{content}} 已写入 {path} 文件")
    except Exception as e:
        logger.info(f"将 {name} 的数据: {content} 写入到文件 {path} 时出错: {e}")


def read_json(path: str):

    """读取 json"""

    json_data = ""
    try:
        with open(path, "r") as f:
            json_data = json.load(f)
        logger.info(f"json 文件 {path} 读取成功: {json_data}")
    except Exception as e:
        logger.error(f"json 文件 {path} 读取失败: {e}")
    return json_data