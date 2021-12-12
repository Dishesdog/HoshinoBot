# -*- coding: utf-8 -*-

import time
import httpx
import random
from hoshino import util, config
import json

from hoshino import Service, priv, util
from hoshino.config.path_config import TEMPLATE_PATH
from hoshino.server.db.utils.point import add_random_points

# https://www.bigfun.cn/api/feweb?target=kan-gong-guild-report/a&date=
# https://www.bigfun.cn/api/feweb?target=kan-gong-guild-report/a&date=2021-10-10

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Cookie': 'sid=huvq63d8; DedeUserID=27213553; DedeUserID__ckMd5=6207d7f289613ef0; _csrf=woI0gHdxxEkr-bxkWJ2dstqC; UM_distinctid=17daca49d3b43d-0a245f86efe6f5-133f6452-1ea000-17daca49d3d3ef; CNZZDATA1275376637=30078234-1639274403-%7C1639274403; b_lsid=E58ACD7B_17DACA4A115; buvid_fp=; SESSDATA=653e61fd%2C1654831058%2C2eeef*c1; bili_jct=9d7b15232258997b794650e158916a50; b_nut=1639279058; session-api=p9dn8ds336qah3ak35nhffhpl3; user-info=4363226',
    'If-None-Match': 'W/"9b8-nQB0z3AFrIrhUXJ6VHxxrdSRPdE"'
}


# 工会成员
async def get_member():
    url = "https://www.bigfun.cn/api/feweb?target=kan-gong-guild-log-filter/a"

    async with httpx.AsyncClient(headers=headers) as client:
        resp = await client.get(url=url)
    return resp.json()["data"]["member"]


#  当日报刀
async def get_report():
    url = "https://www.bigfun.cn/api/feweb?target=kan-gong-guild-report/a&date="

    async with httpx.AsyncClient(headers=headers) as client:
        resp = await client.get(url=url)
    return resp.json()["data"]["member"]
