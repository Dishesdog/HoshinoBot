import json
import os

# 存储文件夹
data_path = os.path.dirname(__file__)


class Util:

    # 判断是否存在
    @classmethod
    def existsFile(cls, file):
        exists = os.path.exists(data_path + '/' + file)
        return exists

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
