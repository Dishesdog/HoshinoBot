# -*- coding: utf-8 -*-

import aiohttp

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
    'Cookie': '_csrf=ke-hyvaHJ04x4Z70xEpupm4p; b_lsid=524C6A22_180F40D0A6D; sid=9crlwp8d; buvid3=5E82BB75-033F-2E5F-90DF-2801010DB0F137976infoc; b_nut=1653361937; buvid4=79B172C6-B25A-B4AC-CAA2-2C0A813BC7D237976-022052411-jRbf6X/z8RBGMV5FR+uM8Q%3D%3D; b_timer=%7B%22ffp%22%3A%7B%22.fp.risk_5E82BB75%22%3A%22180F40D0F54%22%7D%7D; buvid_fp=21cb39364d0d2f3e894ec5f1ad07b260; DedeUserID=27213553; DedeUserID__ckMd5=6207d7f289613ef0; SESSDATA=f0b52612%2C1668913955%2C56bd5*51; bili_jct=45ec36a785c06fd04c109e21d4d2cbfb; session-api=7larcfq6oaksud8tidippa9plc',
    'If-None-Match': 'W/"9b8-nQB0z3AFrIrhUXJ6VHxxrdSRPdE"'
}


# 工会成员
async def get_member():
    async with aiohttp.TCPConnector(verify_ssl=False) as connector:
        async with aiohttp.request(
                method='GET',
                url="https://www.bigfun.cn/api/feweb?target=kan-gong-guild-log-filter/a",
                connector=connector,
                headers=headers,
        ) as resp:
            res = await resp.json()
    data = res['data']
    member = data['member']
    return member


# boss 状态
async def get_boss_info():
    async with aiohttp.TCPConnector(verify_ssl=False) as connector:
        async with aiohttp.request(
                method='GET',
                url="https://www.bigfun.cn/api/feweb?target=kan-gong-guild-boss-info/a",
                connector=connector,
                headers=headers,
        ) as resp:
            res = await resp.json()
    data = res['data']
    return data['boss']


#  当日报刀
async def today_report():
    async with aiohttp.TCPConnector(verify_ssl=False) as connector:
        async with aiohttp.request(
                method='GET',
                url="https://www.bigfun.cn/api/feweb?target=kan-gong-guild-report/a&date=",
                connector=connector,
                headers=headers,
        ) as resp:
            res = await resp.json()
    data = res['data']
    return data


async def getData():
    # 默认
    url = "https://www.bigfun.cn/api/feweb?target=kan-gong-guild-log/a&date=&user_id=&page=1&size=15"
    # 日期筛选
    url = "https://www.bigfun.cn/api/feweb?target=kan-gong-guild-log/a&date=2022-07-28&user_id=&page=1&size=15"
    # 用户筛选
    url = "https://www.bigfun.cn/api/feweb?target=kan-gong-guild-log/a&date=&user_id=27213553&page=1&size=15"

    url = "https://www.bigfun.cn/api/feweb?target=kan-gong-guild-boss-info/a"
