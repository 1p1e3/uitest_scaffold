"""
各个目录的路径，基于 pathlib 而非 os
Paths of various directories, based on pathlib rather than os.
"""

from pathlib import Path

# 框架根目录
root_path = Path(__file__).resolve().parents[1]

# 配置目录
conf_path = root_path.joinpath("conf")

# 工具包目录
utils_path = root_path.joinpath("utils")

# 核心包目录
core_path = root_path.joinpath("core")

# 日志和报告等输出文件存储目录
output_path = root_path.joinpath("output")

# 登录态数据存储路径
cookies_path = core_path.joinpath("auth").joinpath("cookies.json")

# PageObject 页面类目录
pages_path = root_path.joinpath("pages")

# 测试用例目录
test_cases_path = root_path.joinpath("test_cases")






