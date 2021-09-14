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
    ps = []
    # for _ in range(4):
    #     ps.append(min(prop, 8))
    #     prop -= ps[-1]
    tmp = prop
    while True:
        for i in range(0, 4):
            if i == 3:
                ps.append(tmp)
            else:
                if tmp >= 10:
                    ps.append(random.randint(0, 10))
                else:
                    ps.append(random.randint(0, tmp))
                tmp -= ps[-1]
        if ps[3] < 10:
            break
        else:
            tmp = prop
            ps.clear()
    return {
        'CHR': ps[0],
        'INT': ps[1],
        'STR': ps[2],
        'MNY': ps[3]
    }


#
# @sv.on_fullmatch(("/remake", "人生重来"))
# async def remake(bot, ev: CQEvent):
#     pic_list = []
#     mes_list = []
#
#     Life.load(join(FILE_PATH, 'data'))
#     while True:
#         life = Life()
#         life.setErrorHandler(lambda e: traceback.print_exc())
#         life.setTalentHandler(lambda ts: random.choice(ts).id)
#         life.setPropertyhandler(genp)
#         flag = life.choose()
#         if flag:
#             break
#
#     name = ev["sender"]['card'] or ev["sender"]["nickname"]
#     choice = 0
#     person = name + "本次重生的基本信息如下：\n\n【你的天赋】\n"
#     for t in life.talent.talents:
#         choice = choice + 1
#         person = person + str(choice) + "、天赋：【" + t.name + "】" + " 效果:" + t.desc + "\n"
#
#     person = person + "\n【基础属性】\n"
#     person = person + "   美貌值:" + str(life.property.CHR) + "  "
#     person = person + "智力值:" + str(life.property.INT) + "  "
#     person = person + "体质值:" + str(life.property.STR) + "  "
#     person = person + "财富值:" + str(life.property.MNY) + "  "
#     pic_list.append("这是" + name + "本次轮回的基础属性和天赋:")
#     pic_list.append(ImgText(person).draw_text())
#
#     await bot.send(ev, "你的命运正在重启....", at_sender=True)
#
#     res = life.run()  # 命运之轮开始转动
#     mes = '\n'.join('\n'.join(x) for x in res)
#     pic_list.append("这是" + name + "本次轮回的生平:")
#     pic_list.append(ImgText(mes).draw_text())
#
#     sum = life.property.gensummary()  # 你的命运之轮到头了
#     pic_list.append("这是" + name + "本次轮回的评价:")
#     pic_list.append(ImgText(sum).draw_text())
#
#     for img in pic_list:
#         data = {
#             "type": "node",
#             "data": {
#                 "name": "色图机器人",
#                 "uin": "2289875995",
#                 "content": img
#             }
#         }
#         mes_list.append(data)
#
#     await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)


@sv.on_fullmatch(("人生重启", "人生重来"))
async def restart(bot, ev: CQEvent):
    Life.load(join(FILE_PATH, 'data'))
    while True:
        life = Life()
        life.setErrorHandler(lambda e: traceback.print_exc())
        life.setTalentHandler(lambda ts: random.choice(ts).id)
        life.setPropertyhandler(genp)
        flag = life.choose()
        if flag:
            break

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
