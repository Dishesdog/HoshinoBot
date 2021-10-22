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
    'Cookie': 'DedeUserID=27213553; DedeUserID__ckMd5=6207d7f289613ef0; _csrf=vEVPVPyfF6OU-sh6rj3NPiqH; UM_distinctid=17ca7b5dc9a661-0c4dd1c51ff5a2-123b6650-384000-17ca7b5dc9b87e; CNZZDATA1275376637=916080164-1634899450-%7C1634899450; SESSDATA=508df785%2C1650453306%2C919c2%2Aa1; bili_jct=96aae1e292b1f118c5900a8bbe89b1e6; sid=6hvjnp9c; user-info=4363226; session-api=1ujlaprkg1usufdi5jsc8djvmv',
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
