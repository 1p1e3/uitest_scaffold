"""
数据库相关操作, 还未测试是否正常
DB Methods.

Beta Version, Not verified.
"""

import mysql.connector
import redis
from pymongo import MongoClient


from utils.logger import Logger

logger = Logger().get_logger()


class Mysql:
    def __init__(self, mysql_instance: dict):

        """
        初始化数据库链接
        :param mysql_instance: 数据库实例信息
        """

        try:
            self.conn = mysql.connector.connect(mysql_instance)
            logger.info("数据库 {} 连接成功".format(mysql_instance.get('host')))
        except mysql.connector.Error as err:
            logger.error("数据库 {} 连接出错: {}".format(mysql_instance.get('host'), err))
        self.cursor = self.conn.cursor()

    def query(self, sql: str, params: tuple):

        """查询操作"""

        result = self.cursor.execute(sql, params)
        self.conn.commit()
        """其他操作"""

    def close(self):

        """关闭连接"""

        self.cursor.close()
        self.conn.close()


class Redis:
    def __init__(self, redis_instance):
        try:
            self.r = redis.Redis(**redis_instance)
        except redis.exceptions.ConnectionError as e:
            logger.error("redis {} 连接失败: {}".format(redis_instance.get('host'), e))


    def query(self, name: str):
        value = self.r.get(name)
        """后续操作"""

    def close(self):
        self.r.close()



class MongoDB:
    def __init__(self, mongodb_instance: dict, db_name: str, collection_name: str):
        try:
            self.client = MongoClient(**mongodb_instance)
        except Exception as e:
            logger.error("MongoDB {} 连接失败: {}".format(mongodb_instance.get('host'), e))
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]


    def query(self, params: dict):
        self.collection.find(params)
        """后续操作"""


    def close(self):
        self.client.close()

