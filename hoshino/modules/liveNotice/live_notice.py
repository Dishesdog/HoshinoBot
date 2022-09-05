import time
from os import path

from lxml import etree
from nonebot import CommandSession
import requests
import re
from hoshino.service import Service, priv
from hoshino.modules.liveNotice._util import load_config, save_config, broadcast, RSS


class Live(RSS):
    def __init__(self, route: str):
        super().__init__()
        self.route = route
        self.latest_time = ''

    def parse_xml(self):
        rss = etree.XML(self.xml)
        items = rss.xpath('/rss/channel/item')
        data = {}
        tuber = rss.xpath('/rss/channel')[0].find('./title').text
        data['tuber'] = tuber
        if items:
            i = items[0]
            data['link'] = i.find('./link').text.strip()
            data['title'] = i.find('./title').text.strip()
            data['latest_time'] = i.find('./pubDate').text.strip()
        return data


class BiliLive:
    def __init__(self, rId):
        self.platform = '哔哩哔哩'
        self.room_id = rId
        self.latest_time = ''


class DouyuLive:
    def __init__(self, rId):
        self.platform = '斗鱼'
        self.room_id = rId
        self.latest_time = ''

    def checkLive(self, rId):
        url = 'https://m.douyu.com/' + str(rId)
        text = requests.get(url).text
        for i in text.split("\n"):
            regex = re.compile(r"var \$ROOM = ([^']*)")
            match = regex.search(i)
            if match:
                res = dict(eval(match.group(1)))
                return res
        return None


async def notice(rId, msg):
    groups = _subscribes[str(rId)]['subs_groups']
    await broadcast(msg, groups=groups)


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

subs_path = path.join(path.dirname(__file__), 'subs.json')
_subscribes = load_config(subs_path)
_lives = []
for subs in _subscribes:
    platform = _subscribes[subs]['platform']
    room_id = _subscribes[subs]['room']
    latest_time = _subscribes[subs]['latest_time']
    if platform == 'bilibili':
        bl = BiliLive(room_id)
        bl.latest_time = latest_time
        _lives.append(bl)
    elif platform == 'douyu':
        dl = DouyuLive(room_id)
        dl.latest_time = latest_time
        _lives.append(dl)


@sv.scheduled_job('cron', minute='*', second='1')
async def check_live():
    for lv in _lives:
        isLive = 0
        avatar = ""
        title = ""
        opTm = 0
        link = ""
        if lv.platform == "斗鱼":
            res = lv.checkLive(room_id)
            if res:
                avatar = res.get('avatar')
                isLive = res.get('isLive')
                title = res.get('roomName')
                opTm = res.get('showTime')
                link = "www.douyu.com/" + str(room_id)
        else:
            pass

        if isLive:
            latest_time = opTm
            if latest_time != lv.latest_time:
                lv.latest_time = latest_time
                global _subscribes
                _subscribes[str(lv.room_id)]['latest_time'] = latest_time
                save_config(_subscribes, subs_path)
                sv.logger.info(f'检测到{lv.platform}{lv.room_id}直播间开播了')
                await notice(lv.room_id, f'开播提醒=========\n{avatar}\n{title}\n{link}')
        else:
            # 未开播
            pass


@sv.on_command('live', aliases='订阅直播推送', only_to_me=False)
async def subscribe(session: CommandSession):
    session.get('platform', prompt='请选择订阅的平台，目前支持哔哩哔哩和斗鱼')
    platform = ""
    if session.state['platform'] == '哔哩哔哩' or session.state['platform'] == 'bilibili':
        platform = 'bilibili'
    elif session.state['platform'] == '斗鱼' or session.state['platform'] == 'douyu':
        platform = 'douyu'
    else:
        del session.state['platform']
        session.pause('参数错误，请重新输入')
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
            "platform": platform,
            "room": int(room),
            "subs_groups": [gid],
            "latest_time": ""
        }
        lv = BiliLive(int(room))
        global _lives
        _lives.append(lv)
    if save_config(_subscribes, subs_path):
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
            save_config(_subscribes, subs_path)
            sv.logger.info(f'成功取消直播间{room}的开播提醒')
            await session.send(f'成功取消直播间{room}直播提醒')
        else:
            gid = session.event['group_id']
            _subscribes[room]['subs_groups'].remove(gid)
            save_config(_subscribes, subs_path)
            await session.send(f'成功取消直播间{room}直播提醒')
