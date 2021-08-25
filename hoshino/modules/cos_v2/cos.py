# -*- coding: utf-8 -*-
from nonebot.exceptions import CQHttpError
from aiocqhttp.message import MessageSegment
from hoshino import R, Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter
from hoshino.typing import CQEvent
from .cos_util import Util

_max = 5  # 每人日调用上限(次)
_maxLmt = DailyNumberLimiter(_max)

_cd = 3  # 调用间隔冷却时间(s)
_fLmt = FreqLimiter(_cd)

#  启动的时候初始化图片字典
Util.generate()

sv_help = '''
- [cos/Cos/COS]
- [cos状态] 查看统计状态
- [补充次数] 加个钟@aaa
'''.strip()

sv = Service(
    name='cos_v2',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # 是否可见
    enable_on_default=True,  # 是否默认启用
    bundle='娱乐',  # 属于哪一类
    help_=sv_help  # 帮助文本
)


@sv.on_fullmatch(["帮助-cos"])
async def help_cos_v2(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)


@sv.on_fullmatch('cos状态')
async def check_local_status(bot, ev):
    #  每次检测本地状态时 重新构建字典
    Util.generate()
    #  获取涩图路径下所有文件数量
    image_num = Util.getImgCount()

    gid = ev['group_id']

    msg = '这也是你能看的？赶紧爬!!'
    if priv.check_priv(ev, priv.SUPERUSER):
        total, sp = Util.getStat(gid)
        text1 = f'【数据检查】：本地图片的存量为:{image_num}张\n'
        text2 = f'【设定情况】：每日上限为：{_max}次,冷却为：{_cd}秒\n'
        text3 = f'【调用情况】：本群已调用{total}次\n'
        text4 = f'【涩批头子】：还没有人荣获涩批头子称号'
        if int(sp) > 0:
            text4 = f'【涩批头子】：{MessageSegment.at(int(sp))} 荣获涩批头子称号'
        msg = text1 + text2 + text3 + text4

    await bot.send(ev, msg)


@sv.on_fullmatch(('cos', 'COS', 'Cos'))
async def getPic(bot, ev):
    uid = ev['user_id']
    gid = ev['group_id']
    if not _maxLmt.check(uid):
        EXCEED_NOTICE = f'您已经冲过{_max}次了，买个营养快线去找管理PY重置次数吧！'
        await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        return
    if not _fLmt.check(uid):
        await bot.send(ev, f"你不需要休息么", at_sender=True)
        return

    _fLmt.start_cd(uid)
    _maxLmt.increase(uid)

    pic = Util.getImg()

    # 记录统计
    Util.count_gid_uid(gid, uid)
    pic = R.img('cos/', pic)
    try:
        await bot.send(ev, pic.cqcode)
    except CQHttpError:
        await bot.send(ev, '发不出去勒...')


@sv.on_prefix(('加个钟', '补魔'))
async def reset(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.send(ev, '这是你能加的? 赶紧爬!!')
        return
    count = 0
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            uid = int(m.data['qq'])
            _maxLmt.reset(uid)
            count += 1
    if count:
        await bot.send(ev, f"已为{count}位用户重置次数！")
