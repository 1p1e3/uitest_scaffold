"""
群消息通知机器人，发送测试结果通知
Group Notification Bot for Sending Test Results
"""

import requests

from conf.basic_data_conf import feishu_bot_api
from utils.logger import Logger

logger = Logger().get_logger()

class BotMsg:
    # 飞书、企微、钉钉等群机器人 api
    your_api = feishu_bot_api

    headers = {
        "Content - Type": "application / json"
    }

    @classmethod
    def test_result_notify(cls, msg: dict):

        # 飞书自定义机器人：https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot
        # 企微群机器人：https://developer.work.weixin.qq.com/document/path/91770
        # 钉钉：https://open.dingtalk.com/document/orgapp/custom-robots-send-group-messages

        # 下面的请求体是以飞书的为例，企微、钉钉的参考查看对应的 api 文档
        body = {
            "msg_type": "post",
            "content": msg
        }
        r = requests.post(url=cls.your_api, headers=cls.headers, json=body)
        response = r.json()

        """
        后续可以根据响应数据判断消息发送是否成功
        """