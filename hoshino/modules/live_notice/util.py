import json
import os
from hoshino import config

# 存储文件夹
data_path = config.DATA_PATH + 'modules/live_notice/'


class BiliLive:
    def __init__(self, rid):
        self.platform = '哔哩哔哩'
        self.room_id = rid


class Util:

    @classmethod
    def generate(cls):
        _subscribes = cls.readFile('subs.json')
        _lives = []
        for subs in _subscribes:
            room_id = _subscribes[subs]['room']
            latest_time = _subscribes[subs]['latest_time']
            bl = BiliLive(room_id)
            bl.latest_time = latest_time
            _lives.append(bl)

        return _subscribes, _lives

    # 写入文件
    @classmethod
    def saveFile(cls, data, file):
        f = open(data_path + '/' + file, 'w', encoding='utf8')
        json.dump(data, f)
        return True

    # 读取文件
    @classmethod
    def readFile(cls, file):
        if os.path.exists(data_path + '/' + file):
            f = open(os.path.join(data_path, file), mode='r', encoding='utf-8')
            return json.load(f)
        return None
