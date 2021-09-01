# -*- coding: utf-8 -*-
import os
import time
import random
from hoshino import R, Service, priv, util
from hoshino.server.db.utils.point import add_random_points
from .data_source import get_acg_image, get_stick, get_greet, get_msg
from hoshino.config.path_config import TEMPLATE_PATH
from nonebot.message import MessageSegment
import io, base64

sv_help = '''
- [签到]
'''.strip()

sv = Service(
    name='每日签到',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # 是否可见
    enable_on_default=True,  # 是否默认启用
    bundle='娱乐',  # 属于哪一类
    help_=sv_help  # 帮助文本
)


@sv.on_fullmatch(["帮助-签到"])
async def help_cos_v2(bot, ev):
    await bot.send(ev, sv_help)


@sv.on_fullmatch('签到')
async def check_local_status(bot, ev):
    user_id = ev.user_id

    info = await bot.get_group_member_info(
        group_id=ev.group_id,
        user_id=user_id,
        no_cache=True
    )
    name = info['card'] or info['nickname']

    img = await get_card(name, user_id)

    bio = io.BytesIO(img)
    base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()
    msg = f"[CQ:image,file={base64_str}]"
    await bot.send(ev, msg)


async def get_card(user_name: str, user_id: int):
    stick = await get_stick(user_id)
    acg_url = await get_acg_image()

    day_time = time.strftime(r"%m/%d", time.localtime())
    date = time.strftime(r"%Y-%m-%d", time.localtime())
    random.seed()
    cardname = random.choice(["card1"])
    with open(f"{TEMPLATE_PATH}check_in/{cardname}.html", "r", encoding="utf-8") as f:
        template = str(f.read())

    filename = f"temp-card-{user_id}"

    if os.path.isfile(f"{TEMPLATE_PATH}/check_in/temp/{filename}.html"):
        modifiedTime = time.localtime(
            os.stat(f"{TEMPLATE_PATH}/check_in/temp/{filename}.html").st_mtime
        )
        mtime = time.strftime(r"%Y%m%d", modifiedTime)
        ntime = time.strftime(r"%Y%m%d", time.localtime(time.time()))
        if mtime != ntime:
            points = await add_random_points(user_id, 20)
            template = template.replace("[points]", str(points))
        else:
            template = template.replace("[points]", "0(已经签到过啦)")
    else:
        points = await add_random_points(user_id, 20)
        template = template.replace("[points]", str(points))

    template = template.replace("static/", "../static/")
    template = template.replace("[acg_url]", acg_url)
    template = template.replace("[greet]", await get_greet())
    template = template.replace(
        "[msg_of_the_day]", (await get_msg(user_id))["SENTENCE"]
    )
    template = template.replace(
        "[avatar_url]", f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640"
    )
    template = template.replace("[day_time]", day_time)
    template = template.replace("[date]", date)
    template = template.replace("[user_name]", user_name)
    template = template.replace("[luck-status]", stick["FORTUNE_SUMMARY"])
    template = template.replace("[star]", stick["LUCKY_STAR"])
    template = template.replace("[comment]", stick["SIGN_TEXT"])
    template = template.replace("[resolve]", stick["UN_SIGN_TEXT"])

    with open(
            f"{TEMPLATE_PATH}check_in/temp/{filename}.html", "w", encoding="utf-8"
    ) as f:
        f.write(template)

    return await generate_pic(filename)


async def generate_pic(filename: str):
    browser = await util.browser.get_browser()
    page = await browser.new_page()
    path = f"file://{TEMPLATE_PATH}check_in/temp/{filename}.html"
    await page.goto(path)
    card = await page.query_selector(".card")
    assert card is not None
    img = await card.screenshot(type="png")
    await page.close()
    return img
