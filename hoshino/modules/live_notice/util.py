import json
import os
import hoshino

# 存储文件夹
data_path = hoshino.config.DATA_DIR + 'modules/live_notice/'


class BiliLive:
    def __init__(self, rid):
        self.platform = '哔哩哔哩'
        self.room_id = rid


class Util:

    @classmethod
    def generate(cls):
        subs_path = data_path + 'subs.json'
        _subscribes = cls.readFile(subs_path)
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

    # 读取文件
    @classmethod
    def readFile(cls, file):
        if os.path.exists(data_path + '/' + file):
            f = open(os.path.join(data_path, file), mode='r', encoding='utf-8')
            return json.load(f)
        return None

    @classmethod
    def count_gid_uid(cls, gid, uid):
        uid = str(uid)
        gid = str(gid)
        """
        记录群员使用数据
        """
        file = gid + '_count.json'
        data = cls.readFile(file)
        if data is None:
            data = {
                'count': 1,
                'userMap': {
                    uid: 1
                }
            }
        else:
            if uid not in data['userMap']:
                data['userMap'][uid] = 1
            else:
                data['userMap'][uid] = data['userMap'][uid] + 1
            data['count'] = data['count'] + 1

        #  存储数据
        cls.saveFile(data, os.path.join(data_path, file))

    @classmethod
    def getStat(cls, gid):
        file = str(gid) + '_count.json'
        data = cls.readFile(file)
        if data is None:
            return 0, 0

        userMap = data['userMap']
        count = data['count']
        sp = max(userMap, key=lambda k: userMap[k])
        return count, sp, userMap[sp]
