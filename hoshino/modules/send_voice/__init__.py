import os
import random

import hoshino.msgBuild
from hoshino import R, Service, priv, util, config, msgBuild
from hoshino.typing import MessageSegment, CQHttpError, CQEvent, HoshinoBot

sv_help = """
 - 钉宫骂我 [O]
 - 真寻骂我 [x]
 - 亚托莉   [x]
"""

sv = Service(
    name='语音',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # 是否可见
    enable_on_default=True,  # 是否默认启用
    bundle='娱乐',  # 属于哪一类
    help_=sv_help  # 帮助文本
)


@sv.on_fullmatch('钉宫骂我')
async def DingGong(bot: HoshinoBot, ev: CQEvent):
    voice = random.choice(os.listdir(config.VOICE_PATH + "dinggong/"))
    result = msgBuild.record(voice, "dinggong")
    await bot.send(ev, result)
    await bot.send(ev, voice.split("_")[1])
