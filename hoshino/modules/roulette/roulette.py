from aiocqhttp.message import MessageSegment
from hoshino.service import Service, priv
from hoshino.typing import HoshinoBot, CQEvent as Event
from .roulette_source import interact, ActSession
from .roulette_data import dataObj
from hoshino.util import silence
from random import randint, shuffle, choice
from itertools import cycle

sv_help = """
[1] 输入 轮盘赌 开启游戏
[2] 输入 检测轮盘赌 查询数据
"""

sv = Service(
    name='轮盘赌',
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # 是否可见
    enable_on_default=True,  # 是否默认启用
    bundle='娱乐',  # 属于哪一类
    help_=sv_help  # 帮助文本
)

ydie = [
    "很不幸，你死了......",
    "砰...很不幸，你死了......",
    "你死了...",
    "很不幸，你死了......",
    "你扣下了扳机\n你死了...",
    "你拿着手枪掂了掂，你赌枪里没有子弹\n然后很不幸，你死了...",
    "你是一个有故事的人，但是子弹并不想知道这些，它只看见了白花花的脑浆\n你死了",
    "你没有想太多，扣下了扳机。你感觉到有什么东西从你的旁边飞过，然后意识陷入了黑暗\n你死了",
    "大多数人对自己活着并不心存感激，但你不再是了\n你死了...",
    "你举起了枪又放下，然后又举了起来，你的内心在挣扎，但是你还是扣下了扳机，你死了...",
    "你开枪之前先去吃了杯泡面\n然后很不幸，你死了...",
    "你对此胸有成竹，你曾经在精神病院向一个老汉学习了用手指夹住子弹的功夫\n然后很不幸你没夹住手滑了，死了...",
    "今天的风儿很喧嚣，沙尘能让眼睛感到不适。你去揉眼睛的时候手枪走火，贯穿了你的小腹。然后很不幸，你死了...",
    "我会死吗？我死了吗？你正这样想着\n然后很不幸，你死了...",
    "漆黑的眩晕中，心脏渐渐窒息无力，彻骨的寒冷将你包围\n很不幸，你死了...",
]

ylive = [
    "你活了下来，下一位",
    "你扣动扳机，无事发生\n你活了下来",
    "你自信的扣动了扳机，正如你所想象的那样\n你活了下来，下一位",
    "你感觉命运女神在向你招手\n然后，你活了下来，下一位",
    "你吃了杯泡面发现没有调料，你觉得不幸的你恐怕是死定了\n然后，你活了下来，下一位",
    "人和人的体质不能一概而论，你在极度愤怒下，扣下了扳机。利用扳机扣下和触发子弹的时间差，手指一个加速硬生生扣断了它。\n然后，你活了下来，下一位",
    "你曾经在精神病院向一个老汉学习了用手指夹住子弹的功夫\n然后，子弹并没有射出，你活了下来，下一位",
    "你曾经在精神病院向一个老汉学习过用手指夹住射出子弹的功夫，在子弹射出的一瞬间，你把他塞了回去\n你活了下来，下一位",
]


@sv.on_fullmatch(["帮助-轮盘赌"])
async def helper(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)


@sv.on_fullmatch(('轮盘赌', '俄罗斯轮盘赌'))
async def roulette(bot: HoshinoBot, ev: Event):
    try:
        session = ActSession.from_event('俄罗斯轮盘赌', ev, max_user=3, usernum_limit=True)
        interact.add_session(session)
        dataObj.incrJoinNum(ev.group_id, ev.user_id)
        await bot.send(ev, '游戏开始,目前有1位玩家，还缺1名玩家，发送"参与轮盘赌"加入游戏')
    except ValueError as e:
        await bot.finish(ev, f'{e}')


@sv.on_fullmatch('参与轮盘赌')
async def join_roulette(bot: HoshinoBot, ev: Event):
    session = interact.find_session(ev, name='俄罗斯轮盘赌')
    if not session:  # session未创建
        await bot.send(ev, '游戏未创建，发送轮盘赌创建游戏')
        return  # 不处理
    if session.count_user() >= 3:
        await bot.send(ev, f'目前已有3位玩家,发送“开始”进行游戏')

    try:
        interact.join_session(ev, session)
        dataObj.incrJoinNum(ev.group_id, ev.user_id)
        await bot.send(ev, f'成功加入,目前有{session.count_user()}位玩家,发送“开始”进行游戏')

    except ValueError as e:
        await bot.finish(ev, f'{e}')


@interact.add_action('俄罗斯轮盘赌', (f'{MessageSegment.face(169)}', '开枪'))
async def fire(ev: Event, session: ActSession):
    if not session.state.get('started'):
        await session.finish(ev, '请先发送“开始”进行游戏')

    if not session.pos:
        session.state['pos'] = randint(1, 6)  # 拨动轮盘，pos为第几发是子弹 """
    if not session.state.get('times'):
        session.state['times'] = 1

    if ev.user_id != session.state.get('turn'):
        return
        # await session.finish(event, '现在枪不在你手上哦~')

    pos = session.pos
    times = session.times
    if pos == times:  # shoot
        session.close()
        dataObj.incrDeadNum(ev.group_id, ev.user_id)  # 增加死亡数
        await session.send(ev, choice(ydie))
        await silence(ev, 120)
    elif times == 5:
        session.close()
        user = session.rotate.__next__()
        dataObj.incrKillNum(ev.group_id, ev.user_id)  # 增加击杀数
        dataObj.incrDeadNum(ev.group_id, user)  # 增加死亡数
        await session.send(ev, f'你长舒了一口气，并反手击毙了{MessageSegment.at(user)}')
        await session.bot.set_group_ban(group_id=ev.group_id, user_id=user, duration=120)
    else:
        session.state['times'] += 1
        session.state['turn'] = session.rotate.__next__()
        await session.send(ev, f'{choice(ylive)},轮到{MessageSegment.at(session.state["turn"])}开枪')


@interact.add_action(('俄罗斯轮盘赌', '开始'))
async def start_roulette(event: Event, session: ActSession):
    if session.count_user() < 2:
        await session.finish(event, '人数不足')

    if not session.state.get('started'):
        session.state['started'] = True
        rule = """
        轮盘容量为6，但只填充了一发子弹，请参与游戏的双方轮流发送开枪，枪响结束
        """.strip()
        if not session.rotate:  # user轮流
            shuffle(session.users)
            session.state['rotate'] = cycle(session.users)
        if not session.turn:
            session.state['turn'] = session.rotate.__next__()
        await session.send(event, f'游戏开始,{rule}现在请{MessageSegment.at(session.state["turn"])}开枪')
    else:
        await session.send(event, '游戏已经开始了')


@sv.on_fullmatch(["靶子王你飘了啊"])
async def force(bot: HoshinoBot, ev: Event):
    if priv.check_priv(ev, priv.SUPERUSER):
        msg = f"就在这时旁边正在进行的一场决斗中一颗流弹击中了你,你死了{MessageSegment.at(502199815)}"
        await bot.send(ev, msg)


@sv.on_fullmatch(["检测轮盘赌"])
async def checkCount(bot: HoshinoBot, ev: Event):
    gid = ev.group_id
    data = dataObj.getStat(gid)

    text1 = f"【总次数】：本群已玩过{data['total']}次\n"
    text2 = f'【场次王】：本群还没有产生场次王\n'
    text3 = f'【击杀王】：本群还没有产生击杀王\n'
    text4 = f'【吸铁石】：本群还没有产生吸铁石'

    if int(data['join']['id']) > 0:
        text2 = f"【场次王】：{MessageSegment.at(int(data['join']['id']))} 参与 {data['join']['num']}\n"

    if int(data['kill']['id']) > 0:
        text3 = f"【击杀王】：{MessageSegment.at(int(data['kill']['id']))} 击杀 {data['kill']['num']}\n"

    if int(data['dead']['id']) > 0:
        text4 = f"【吸铁石】：{MessageSegment.at(int(data['dead']['id']))} 死亡 {data['dead']['num']}"

    msg = text1 + text2 + text3 + text4
    await bot.send(ev, msg)
