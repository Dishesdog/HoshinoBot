import json
import os
import random
import hoshino

# 当前文件夹
fd = os.path.dirname(__file__)

# 填写你的本地涩图文件夹路径
cos_path = hoshino.config.RES_DIR + 'img/cos/'


class Util:

    # 生成字典
    @classmethod
    def generate(cls):
        """
        生成列表快速获取
        """
        picList = []
        fileList = os.listdir(cos_path)
        for filename in fileList:
            if os.path.isfile(os.path.join(cos_path, filename)):
                picList.append(filename)

        data = {
            'count': len(picList),
            'list': picList
        }
        cls.saveFile(data, os.path.join(fd, 'img.json'))

    # 写入文件
    @classmethod
    def saveFile(cls, data, file):
        f = open(file, 'w')
        json.dump(data, f)

    # 读取文件
    @classmethod
    def readFile(cls, file):
        if os.path.exists(fd + '/' + file):
            f = open(os.path.join(fd, file))
            return json.load(f)
        return None

    # 获取图片
    @classmethod
    def getImg(cls):
        data = cls.readFile('img.json')
        return random.choice(data['list'])

    # 获取总数
    @classmethod
    def getImgCount(cls):
        """
        获取图片数量
        """
        data = cls.readFile('img.json')
        return data['count']

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
        cls.saveFile(data, os.path.join(fd, file))

    @classmethod
    def getStat(cls, gid):
        file = str(gid) + '_count.json'
        data = cls.readFile(file)
        if data is None:
            return 0, 0

        userMap = data['userMap']
        count = data['count']
        sp = max(userMap, key=lambda k: userMap[k])
        return count, sp
