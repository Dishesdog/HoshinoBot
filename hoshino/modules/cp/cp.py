# -*- coding: utf-8 -*-
import json
import os
import random
from hoshino import Service, priv

sv_help = '''
[CP小故事]
- cp A B 生成 A-B的小故事
'''

path = os.path.dirname(__file__)

sv = Service(
    name='CP小故事',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=True,  # 是否默认启用
    bundle='娱乐',  # 属于哪一类
    help_=sv_help  # 帮助文本
)


@sv.on_fullmatch(["帮助-CP小故事"])
async def helper(bot, ev):
    await bot.send(ev, sv_help)


def readInfo(file):
    with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
        return json.loads((f.read()).strip())


def getMessage(bot, userGroup):
    content = readInfo('content.json')
    content = random.choice(content['data']).replace('<攻>', userGroup[0]).replace('<受>', userGroup[1])
    return content


@sv.on_prefix('cp')
async def entranceFunction(bot, ev):
    s = ev.message.extract_plain_text().split(' ')
    try:
        name = s[0]
        name = s[1]
    except:
        return
    await bot.send(ev, getMessage(bot, s))
