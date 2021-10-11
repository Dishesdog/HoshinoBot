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
    'Cookie': 'sid=bh1ih1fp; DedeUserID=27213553; DedeUserID__ckMd5=6207d7f289613ef0; SESSDATA=23babff3%2C1649211361%2C7aa15*a1; bili_jct=0521b4b2803924ee7853a4725c7631f8; _csrf=U64KG7palU0C5WdyGj8jrtkD; UM_distinctid=17c6d7ee8c3b3f-0b695359fa90f6-1d3b6650-384000-17c6d7ee8c4df7; CNZZDATA1275376637=1901681995-1633923033-%7C1633923033; session-api=tabduup3gij5von07u14pcs7m1',
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
