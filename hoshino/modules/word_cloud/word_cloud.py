import datetime
import os
import random
import re

import jieba
import nonebot
import wordcloud
from nonebot import MessageSegment

import hoshino
from hoshino import Service, priv, priv, config
from hoshino.typing import CQEvent

sv_help = '''
- [词云]
- 生成今日词云
'''.strip()

sv = Service(
    name='词云',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    enable_on_default=True,  # 是否默认启用
    bundle='娱乐',  # 属于哪一类
    help_=sv_help  # 帮助文本
)

loadpath = config.CQ_LOG_PATH  # 此处填gocq的logs路径
self_id = config.SELF_ID  # 此处填机器人的QQ号
load_in_path = config.IMAGE_PATH + 'wordcloud/'  # 此处填词云图片保存的路径

tyc_path = os.path.join(os.path.dirname(__file__), 'tyc.txt')
font_path = os.path.join(os.path.dirname(__file__), 'SimHei.ttf')


@sv.on_fullmatch(["帮助-词云"])
async def helper(bot, ev):
    await bot.send(ev, sv_help)


@sv.on_fullmatch('生成今日词云')
async def getByToday(bot, ev: CQEvent):
    if not hoshino.priv.check_priv(ev, hoshino.priv.OWNER):
        await bot.send(ev, message='仅限群主可用', at_sender=True)
        return
    await bot.send(ev, message='正在生成本群今日词云，请耐心等待', at_sender=True)
    gid = ev.group_id
    today = datetime.date.today().__format__('%Y-%m-%d')
    makeFile(today, gid)
    await bot.send(ev, MessageSegment.image(f'file:///{load_in_path}/{today}-{gid}.png'))


@sv.on_fullmatch('生成昨日词云')
async def getByYesterday(bot, ev: CQEvent):
    if not hoshino.priv.check_priv(ev, hoshino.priv.OWNER):
        await bot.send(ev, message='仅限群主可用', at_sender=True)
        return
    await bot.send(ev, message='正在生成本群昨日词云，请耐心等待', at_sender=True)
    gid = ev.group_id
    yesterday = (datetime.date.today() + datetime.timedelta(-1)).__format__('%Y-%m-%d')
    makeFile(yesterday, gid)

    await bot.send(ev, MessageSegment.image(f'file:///{load_in_path}/{yesterday}-{gid}.png'))


def makeFile(day, gid=0):
    logs = open(f"{loadpath}/{day}.log", "r", encoding="utf-8")
    logs.seek(0)
    gid = str(gid)
    msg = ''
    for line in logs.readlines():  # 删除前缀和自己的发言
        if self_id in line or gid not in line:
            continue
        try:
            o = line.split("的消息: ")[1]
            msg += o
        except Exception as e:
            pass
    msg = re.sub('''[a-zA-Z0-9'!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘'！[\\]^_`{|}~\s]+''', "", msg)
    msg = re.sub(
        '[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+',
        '', msg)
    banword = []  # 此处为不显示的删除禁词
    ls = jieba.lcut(msg)  # 制作分词
    stopwords = set()
    content = [line.strip() for line in open(tyc_path, encoding='utf-8').readlines()]
    stopwords.update(content)
    txt = " ".join(ls)
    w = wordcloud.WordCloud(font_path=font_path,
                            max_words=10000, width=1000, height=700,
                            background_color='white', stopwords=stopwords,
                            relative_scaling=0.5, min_word_length=2,
                            color_func=random_color_func  # 词汇上限，宽，高,背景颜色去除停用词(tyc.txt),频次与大小相关度，最小词长,调色
                            )
    w.generate(txt)
    if gid:
        w.to_file(f"{load_in_path}/{day}-{gid}.png")
    else:
        w.to_file(f"{load_in_path}/{day}.png")


def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    if random_state is None:
        random_state = random
    return "hsl(%d, 75%%, 62%%)" % random_state.randint(0, 225)  # 值，饱和度，色相


# 定时任务
@sv.scheduled_job('cron', day='*', hour='23', minute='55')
async def autoSend():
    bot = nonebot.get_bot()
    today = datetime.date.today().__format__('%Y-%m-%d')
    try:
        makeFile(today)
    except Exception as e:
        await bot.send_private_msg(user_id=hoshino.config.SUPERUSERS[2], message=f'{today}词云生成失败,失败原因:{e}')
