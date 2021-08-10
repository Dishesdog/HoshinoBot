# -*- coding:utf-8 -*-
from peewee import *
from hoshino import config

# 建立连接mysql时的必要参数
db = MySQLDatabase('myBot', host=config.MYSQL_HOST, user=config.MYSQL_USER, passwd=config.MYSQL_PWD)


class RepeaterPic(Model):
    id = AutoField(primary_key=True)
    url = CharField()  #
    url_md5 = CharField(unique=True)

    class Meta:
        database = db
        table_name = 'repeater_pic'


# 插入数据
def saveToDb(url, picHash):
    try:
        RepeaterPic.replace(
            url=url,
            url_md5=picHash
        ).execute()
    except Exception as e:
        print(e)
        pass
