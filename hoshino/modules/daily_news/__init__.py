# -*- coding: utf-8 -*-

from hoshino import Service, util, aiorequests
from hoshino.typing import MessageSegment, CQHttpError, CQEvent, HoshinoBot

sv_help = '''
- [每日早报] 启用后会在每天早上发送一份早报
'''.strip()

sv = Service(
    name='每日早报',  # 功能名
    visible=True,  # 是否可见
    enable_on_default=True,  # 是否默认启用
    bundle='任务',  # 属于哪一类
    help_=sv_help  # 帮助文本
)


@sv.on_fullmatch(["帮助-早报"])
async def helper(bot, ev):
    await bot.send(ev, sv_help)


@sv.on_fullmatch(['今日早报'])
async def handnews(bot: HoshinoBot, ev: CQEvent):
    info = await aiorequests.get('http://dwz.2xb.cn/zaob')
    info = await info.json()
    if info['msg'] == 'Success':
        await bot.send(ev, MessageSegment.image(info['imageUrl'], cache=True))
    else:
        sv.logger.error(f'daily news error {info["msg"]}')


@sv.scheduled_job('cron', hour='19', minute='22')
async def autonews():
    try:
        info = await aiorequests.get('http://dwz.2xb.cn/zaob')
        try:
            info = await info.json()
        except:
            print(await info.text)
            raise
        if info['msg'] == 'Success':
            await sv.broadcast(MessageSegment.image(info['imageUrl'], cache=True), 'daily_news')
        else:
            sv.logger.error(f'daily news error {info["msg"]}')
    except CQHttpError as e:
        sv.logger.error(f'daily news error {e}')
        raise
