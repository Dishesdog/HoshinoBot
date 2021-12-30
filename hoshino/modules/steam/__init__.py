from hoshino import Service, get_bot, priv
from .steam_crawler_bot import crawler, url_decide, hey_box
from .xjy import xjy_compare, xjy_result
import os
import json
from .util import Util

sv_help = f'''
本插件有如下指令：
- [今日特惠]：获取今日Steam特惠
- [喜加一资讯]：获取今日喜加一
- [开启 or 关闭喜加一提醒]：开启或关闭在本群的喜加一提醒服务
'''.strip()

FILE_PATH = os.path.join(os.path.dirname(__file__))

url_new = "https://store.steampowered.com/search/results/?l=schinese&query&sort_by=Released_DESC&category1=998&os=win" \
          "&infinite=1&start=0&count=50 "
url_specials = "https://store.steampowered.com/search/results/?l=schinese&query&sort_by=_ASC&category1=998&specials=1" \
               "&os=win&filter=topsellers&start=0&count=50 "

sv = Service(
    name='游戏资讯',
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # 是否可见
    enable_on_default=True,  # 是否默认启用
    bundle='订阅',  # 属于哪一类
    help_=sv_help  # 帮助文本
)


@sv.on_fullmatch('帮助-游戏资讯')
async def bot_help(bot, ev):
    await bot.send(ev, sv_help)


# 匹配关键词发送相关信息，例：今日特惠，发送今日特惠信息，今日新品则发送新品信息
@sv.on_prefix('今日')
async def Gameinfo(bot, ev):
    try:
        mes_list = None
        model = ev.message.extract_plain_text().strip()
        await bot.send(ev, "正在生成合并消息，请稍等片刻！", at_sender=True)
        if model == "新品":
            mes_list = crawler(url_new)
        elif model == "特惠":
            mes_list = crawler(url_specials)
        if mes_list:
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)
    except Exception as e:
        sv.logger.error(f"Error:{e}")
        await bot.send(ev, "哦吼，出错了，请检查主机网络情况、查看运行日志或者再试一遍")


# 后接想要看的资讯条数（阿拉伯数字）
@sv.on_prefix('喜加一资讯')
async def xjy_info(bot, ev):
    if not Util.existsFile('xjy_result.json'):
        try:
            xjy_compare()
        except Exception as e:
            sv.logger.error(f"Error:{e}")
            await bot.send(ev, "哦吼，出错了，请检查主机网络情况、查看运行日志或者再试一遍")
    res = Util.readFile('xjy_result.json')
    num = len(res)
    state1 = xjy_result("Query", int(num))
    mes_list = []
    if "error" in state1:
        sv.logger.error(state1)
        await bot.send(ev, "哦吼，出错了，请检查主机网络情况、查看运行日志或者再试一遍")
        pass
    else:
        if len(state1) <= 2:
            for i in state1:
                await bot.send(ev, message=i)
        else:
            for i in state1:
                data = {
                    "type": "node",
                    "data": {
                        "name": "菜狗",
                        "uin": "2289875995",
                        "content": i
                    }
                }
                mes_list.append(data)
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)


# 这部分直接抄了@H-K-Y(https://github.com/H-K-Y)大佬的原神插件里的一部分代码
group_list = []


def save_group_list():
    with open(os.path.join(FILE_PATH, 'group_list.json'), 'w', encoding='UTF-8') as file:
        json.dump(group_list, file, ensure_ascii=False)


# 检查group_list.json是否存在，没有创建空的
if not os.path.exists(os.path.join(FILE_PATH, 'group_list.json')):
    save_group_list()

# 读取group_list.json的信息
with open(os.path.join(FILE_PATH, 'group_list.json'), 'r', encoding='UTF-8') as f:
    group_list = json.load(f)


# 喜加一提醒开关
@sv.on_fullmatch('开启喜加一提醒')
async def open_remind(bot, ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.send(ev, "你没有权限这么做")
        return
    gid = str(ev.group_id)
    if not (gid in group_list):
        group_list.append(gid)
        save_group_list()
    await bot.send(ev, "喜加一提醒已开启，如有新喜加一信息则会推送")


@sv.on_fullmatch('关闭喜加一提醒')
async def off_remind(bot, ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.send(ev, "你没有权限这么做")
        return
    gid = str(ev.group_id)
    if gid in group_list:
        group_list.remove(gid)
        save_group_list()
    await bot.send(ev, "喜加一提醒已关闭")


# 定时检查是否有新的喜加一信息
@sv.scheduled_job('cron', hour='*', minute='*')
async def xjy_remind():
    bot = get_bot()
    url_list = xjy_compare()
    if "Server Error" in url_list:
        sv.logger.info("访问it之家出错，非致命错误，可忽略")
    elif "error" in url_list:
        sv.logger.error(url_list)
    elif len(url_list) != 0:
        mes = xjy_result("Default", url_list)
        for gid in group_list:
            await bot.send_group_msg(group_id=int(gid), message="侦测到在途的喜加一信息，即将进行推送...")
            for i in mes:
                await bot.send_group_msg(group_id=int(gid), message=i)
    else:
        sv.logger.info("无新喜加一信息")
