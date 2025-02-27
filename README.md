<h1 align="center">uitest_scaffold</h1>

<p align="center">
  <br>简体中文 | <a href="README_EN.md.md">English</a>
</p>

## 说明
一个 UI 自动化测试框架脚手架，基于 Pytest + Playwright 构建。


## 结构
基于 PageObject 模式组织页面类与对应的测试类。

基于 Pytest 组织测试过程和用例。

测试会话开始之前检查登录状态，基于 Playwright 实现登录态 cookie 数据的存储和加载。

测试结束之后使用 Pytest 提供的钩子函数收集并统计测试结果，利用飞书、钉钉、企微等提供的群消息机器人将测试结果同步到工作群内。


## 模块说明
- **conf**: 基础配置，包含路径配置，群消息机器人配置，基础数据配置等
- **core**: 核心模块，包含页面基类，持久化登录认证，浏览器相关实例管理等
- **ouput**: 输出文件存储路径，包含日志，测试报告，截图等
- **pagees**: Page Object 页面类
- **test_cases**: 测试用例
- **utils**: 工具模块，包含日志配置、json 文件处理等
- **conftest.py**: 全局共享配置