import nonebot
from nonebot import CommandSession
from bilibili_api import live
from hoshino.service import Service, priv
from .util import Util, BiliLive
from hoshino.log import new_logger
import asyncio

logger = new_logger('liveNotice', debug=False)

bot = nonebot.get_bot()

sv_help = """
B站直播订阅
"""

sv = Service(
    name='直播推送',
    use_priv=priv.SUPERUSER,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # 是否可见
    enable_on_default=True,  # 是否默认启用
    bundle='订阅',  # 属于哪一类
    help_=sv_help  # 帮助文本
)

_subscribes, _lives = Util.generate()


# 定时任务
@sv.scheduled_job('cron', minute='*', second='1')
async def check_live():
    for lv in _lives:
        await check_bili_live(lv)


#  检测是否开播
async def check_bili_live(lv):
    roomId = lv.room_id
    data = await live.LiveRoom(room_display_id=roomId).get_room_info()
    roomInfo = data.get('room_info')
    if roomInfo.get('live_status') == 1:  # 开播状态
        title = roomInfo['title']
        cover = roomInfo['cover']
        live_start_time = roomInfo['live_start_time']
        link = "https://live.bilibili.com/" + str(roomId)
        # 判断是否是新开播
        if live_start_time != lv.latest_time:
            lv.latest_time = live_start_time
            global _subscribes
            _subscribes[str(roomId)]['latest_time'] = live_start_time
            # 跟新开播时间
            Util.saveFile(_subscribes, 'subs.json')
            sv.logger.info(f'检测到{lv.platform}{lv.room_id}直播间开播了')

            pic = f'[CQ:image,file={cover}]'.format(cover=cover)
            at = f"[CQ:at,qq=all]"
            await broadcast(f'开播提醒{at}\n{pic}\n{title}\n{link}', lv.room_id)
    else:
        # 未开播
        pass


async def broadcast(msg, room_id, sv_name=None):
    groups = _subscribes[str(room_id)]['subs_groups']

    svs = Service.get_loaded_services()
    if not groups and sv_name not in svs:
        raise ValueError(f'不存在服务 {sv_name}')
    if sv_name:
        enable_groups = await svs[sv_name].get_enable_groups()
        send_groups = enable_groups.keys() if not groups else groups
    else:
        send_groups = groups
    for gid in send_groups:
        try:
            await bot.send_group_msg(group_id=gid, message=msg)
            logger.info(f'群{gid}投递消息成功')
            await asyncio.sleep(0.5)
        except Exception as e:
            logger.exception(e)


@sv.on_command('live', aliases='订阅直播推送', only_to_me=False)
async def subscribe(session: CommandSession):
    room = session.get('room', prompt='请输入订阅的房间号')
    if not session.state['room'].isdigit():
        del session.state['room']
        session.pause('参数错误，请重新输入')
    global _subscribes
    gid = session.event['group_id']
    if room in _subscribes.keys():
        if gid not in _subscribes[room]['subs_groups']:
            _subscribes[room]['subs_groups'].append(gid)
        else:
            await session.send('本群已经订阅过该直播间了')
            return
    else:
        _subscribes[room] = {
            "room": int(room),
            "subs_groups": [gid],
            "latest_time": ""
        }
        lv = BiliLive(int(room))
        global _lives
        _lives.append(lv)
    if Util.saveFile(_subscribes, 'subs.json'):
        await session.send('订阅成功')
    else:
        await session.send('订阅失败，请与bot维护中联系')


@sv.on_command('cancel_live', aliases=('取消直播推送', '取消直播提醒'))
async def cancel(session: CommandSession):
    room = session.get('room', prompt='请输入房间号')
    global _subscribes
    global _lives
    if room in _subscribes.keys():
        if len(_subscribes[room]['subs_groups']) == 1:  # 只有一个群订阅该直播
            for lv in _lives[::-1]:
                if lv.room_id == int(room):
                    _lives.remove(lv)
            del _subscribes[room]
            Util.saveFile(_subscribes, 'subs.json')
            sv.logger.info(f'成功取消直播间{room}的开播提醒')
            await session.send(f'成功取消直播间{room}直播提醒')
        else:
            gid = session.event['group_id']
            _subscribes[room]['subs_groups'].remove(gid)
            Util.saveFile(_subscribes, 'subs.json')
            await session.send(f'成功取消直播间{room}直播提醒')
