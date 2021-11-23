import os
import random
import hoshino

from nonebot import *
from hoshino import Service, priv

sv_help = '''- 戳一戳服务'''

sv = Service(
    name='戳一戳',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=True,  # 是否默认启用
    bundle='娱乐',  # 属于哪一类
    help_=sv_help  # 帮助文本
)


@sv.on_fullmatch(["帮助-戳一戳"])
async def helper(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)


@sv.on_notice('notify')
async def poke_(session: NoticeSession):
    sub_type = session.event['sub_type']
    self_id = session.event['self_id']
    target_id = session.event['target_id']
    group_id = session.event['group_id']
    sender_id = session.event['sender_id']

    msgList = [
        "lsp你再戳？",
        "你再戳！",
        "？再戳试试？",
        "我爪巴爪巴，球球别再戳了",
        "你戳你🐎呢？！",
        "有事恁叫我，别天天一个劲戳戳戳！",
        "欸很烦欸！你戳你爹呢",
        "再戳一下试试？",
        "正在关闭对您的所有服务...关闭成功",
        "正在定位您的真实地址...定位成功。轰炸机已起飞",
        "傻狗，别戳了",
        "傻狗，别戳了",
        "傻狗，别戳了",
        "傻狗，别戳了",
        "傻狗，别戳了",
        "傻狗，别戳了",
        "傻狗，别戳了",
        "傻狗，别戳了",
        "傻狗，别戳了",
        "傻狗，别戳了",
    ]
    if sub_type == 'poke':
        if self_id == target_id:
            try:
                await session.bot.set_group_ban(group_id=group_id, user_id=sender_id, duration=120)
                await session.send(random.choice(msgList))
            except Exception as e:
                hoshino.logger.error(f'封禁失败：{e}')
                await session.send(random.choice(msgList))
                return None
