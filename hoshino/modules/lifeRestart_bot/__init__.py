# coding=utf-8
from hoshino import Service, util
from hoshino.typing import CQEvent
from hoshino.config.path_config import TEMPLATE_PATH
from os.path import join

import traceback
import base64
import io
import random
from .Life import Life
from .PicClass import *

sv = Service("人生重来模拟器")


def genp(prop):
    if prop < 1:
        return {'CHR': 0, 'INT': 0, 'STR': 0, 'MNY': 0}
    ps = []
    for i in range(3):
        ps.append(id(i) % (int(prop * 2 / (4 - i)) + 1))
        if 10 < ps[-1]:
            ps[-1] = 10
        prop -= ps[-1]
    if 10 < prop:
        prop += sum(ps)
        ps = [int(prop / 4)] * 3
        prop -= sum(ps)
    return {
        'CHR': ps[0],
        'INT': ps[1],
        'STR': ps[2],
        'MNY': prop
    }


@sv.on_fullmatch(("人生重启", "人生重来"))
async def restart(bot, ev: CQEvent):
    Life.load(join(FILE_PATH, 'data'))
    life = Life()
    life.setErrorHandler(lambda e: traceback.print_exc())
    life.setTalentHandler(lambda ts: random.choice(ts).id)
    life.setPropertyhandler(genp)
    life.choose()

    user_id = ev["sender"]['user_id']
    filename = f"temp-card-{user_id}"

    with open(f'{TEMPLATE_PATH}/lifeRestart/card.html') as f:
        tmp = str(f.read())

    talentText = ''
    for t in life.talent.talents:
        talentText += f"<li class='talentItem'><span class='name'>{t.name}</span><span class='desc'>{t.desc}</span></li>"

    res = life.run()

    lifeList = ""
    for x in res:
        eventText = f"<li><span class='age'>{x[0]}</span>"
        for eventItem in x[1:]:
            eventText += f"{eventItem}<br/>"
        eventText += f"</li>"

        lifeList += eventText

    name = ev["sender"]['card'] or ev["sender"]["nickname"]
    person = name + "本次重生的基本信息如下\n"

    tmp = tmp.replace("static/", "../static/")
    #  头像
    tmp = tmp.replace("[avatar_url]", f"https://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640")
    #  属性
    tmp = tmp.replace('[talentList]', talentText)
    # 事件
    tmp = tmp.replace('[lifeList]', lifeList)

    tmp = tmp.replace('[CHR]', str(life.property.CHR))  # 颜值 charm CHR
    tmp = tmp.replace('[INT]', str(life.property.INT))  # 智力 intelligence INT
    tmp = tmp.replace('[STR]', str(life.property.STR))  # 体质 strength STR
    tmp = tmp.replace('[MNY]', str(life.property.MNY))  # 家境 money MNY
    tmp = tmp.replace('[SPR]', str(life.property.SPR))  # 快乐 spirit SPR
    tmp = tmp.replace('[AGE]', str(life.property.AGE))  # 年龄 age AGE
    tmp = tmp.replace('[SUM]', str(life.property.SUM))  # 年龄 age AGE

    life.property.getSummary()

    tmp = tmp.replace('[CHR_JUDGE]', str(life.property.CHR_JUDGE))  # 颜值 charm CHR
    tmp = tmp.replace('[INT_JUDGE]', str(life.property.INT_JUDGE))  # 智力 intelligence INT
    tmp = tmp.replace('[STR_JUDGE]', str(life.property.STR_JUDGE))  # 体质 strength STR
    tmp = tmp.replace('[MNY_JUDGE]', str(life.property.MNY_JUDGE))  # 家境 money MNY
    tmp = tmp.replace('[SPR_JUDGE]', str(life.property.SPR_JUDGE))  # 快乐 spirit SPR
    tmp = tmp.replace('[AGE_JUDGE]', str(life.property.AGE_JUDGE))  # 年龄 age AGE
    tmp = tmp.replace('[TOTAL_JUDGE]', str(life.property.TOTAL_JUDGE))  # 年龄 age AGE

    with open(f"{TEMPLATE_PATH}/lifeRestart/temp/{filename}.html", "w", encoding="utf-8") as f:
        f.write(tmp)

    img = await generate_pic(filename)
    bio = io.BytesIO(img)
    base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()
    msg = f"[CQ:image,file={base64_str}]"

    mes_list = [
        {
            "type": "node",
            "data": {
                "name": "色图机器人",
                "uin": "2289875995",
                "content": person
            }
        },
        {
            "type": "node",
            "data": {
                "name": "色图机器人",
                "uin": "2289875995",
                "content": msg
            }
        }
    ]
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)
    # await bot.send(ev, msg)


async def generate_pic(filename: str):
    browser = await util.browser.get_browser()
    page = await browser.new_page()
    path = f"file://{TEMPLATE_PATH}lifeRestart/temp/{filename}.html"
    await page.goto(path)
    card = await page.query_selector(".card")
    assert card is not None
    img = await card.screenshot(type="png")
    await page.close()
    return img
