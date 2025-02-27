<h1 align="center">uitest_scaffold</h1>

<p align="center">
  <br>English | <a href="README.md">简体中文</a>
</p>


## Description
A UI automation testing framework scaffold, built on Pytest + Playwright.

## Structure
The pages and corresponding test classes are organized based on the PageObject pattern.

Tests are organized using Pytest to structure the test process and test cases.

Before starting the test session, the login status is checked. Login cookies are stored and loaded using Playwright.

After the tests are completed, Pytest hooks are used to collect and summarize test results. The results are then synchronized to workgroup chat apps like Feishu, DingTalk, and WeCom through their respective message bots.

## Module Explanation
- **conf**: Basic configuration, including path settings, message bot configurations, basic data configurations, etc.
- **core**: Core modules, including page base classes, persistent login authentication, browser instance management, etc.
- **output**: Output file storage paths, including logs, test reports, screenshots, etc.
- **pages**: Page Object classes for pages.
- **test_cases**: Test cases.
- **utils**: Utility modules, including log configuration, JSON file handling, etc.
- **conftest.py**: Global shared configuration.