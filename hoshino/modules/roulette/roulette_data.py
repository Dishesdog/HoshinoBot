import json
import os
from hoshino import config

# 存储文件夹
data_path = config.DATA_PATH + 'modules/roulette/'


class Data:
    def __init__(self):
        if not os.path.exists(data_path):
            os.makedirs(data_path)

    # 读取文件
    @classmethod
    def readFile(cls, file):
        if os.path.exists(data_path + '/' + file):
            f = open(data_path + '/' + file)
            return json.load(f)
        return None

    # 写入文件
    @classmethod
    def saveFile(cls, data, file):
        f = open(data_path + '/' + file, 'w')
        json.dump(data, f)

    @classmethod
    def incrJoinNum(cls, gid, uid):
        uid = str(uid)
        gid = str(gid)
        file = gid + '_count.json'
        data = cls.readFile(file)
        if data is None:
            data = {
                'count': 1,
                'join': {
                    uid: 1
                },
                'kill': {
                    uid: 0
                },
                'dead': {
                    uid: 0
                }
            }
        else:
            if uid not in data['join']:
                data['join'][uid] = 1
            else:
                data['join'][uid] = data['join'][uid] + 1
            data['count'] = data['count'] + 1

        #  存储数据
        cls.saveFile(data, file)

    @classmethod
    def incrKillNum(cls, gid, uid):
        uid = str(uid)
        gid = str(gid)
        file = gid + '_count.json'
        data = cls.readFile(file)
        if uid not in data['kill']:
            data['kill'][uid] = 1
        else:
            data['kill'][uid] = data['kill'][uid] + 1

        #  存储数据
        cls.saveFile(data, file)

    @classmethod
    def incrDeadNum(cls, gid, uid):
        uid = str(uid)
        gid = str(gid)
        file = gid + '_count.json'
        data = cls.readFile(file)
        if uid not in data['dead']:
            data['dead'][uid] = 1
        else:
            data['dead'][uid] = data['dead'][uid] + 1

        #  存储数据
        cls.saveFile(data, file)

    #
    @classmethod
    def getStat(cls, gid):
        file = str(gid) + '_count.json'
        data = cls.readFile(file)

        res = {
            'total': 0,
            'join': {'id': 0, 'num': 0},
            'kill': {'id': 0, 'num': 0},
            'dead': {'id': 0, 'num': 0},
        }
        if data is None:
            return res

        total = data['count']
        joinMap = data['join']
        killMap = data['kill']
        deadMap = data['dead']
        joinId = max(joinMap, key=lambda k: joinMap[k])
        killId = max(killMap, key=lambda k: killMap[k])
        deadId = max(deadMap, key=lambda k: deadMap[k])

        res = {
            'total': total,
            'join': {'id': joinId, 'num': joinMap[joinId]},
            'kill': {'id': killId, 'num': killMap[killId]},
            'dead': {'id': deadId, 'num': deadMap[deadId]},
        }
        return res


dataObj = Data()
