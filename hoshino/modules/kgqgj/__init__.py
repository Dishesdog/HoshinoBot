# -*- coding: utf-8 -*-
import aiohttp
import base64
import io

from hoshino import Service, priv, util
from .data_source import headers

sv_help = '''
- [坎公工会战]
- 报刀 - 当日会战报表
- Boss状态 - Boss状态
- 总伤统计 - 本期伤害统计
'''.strip()

sv = Service(
    name='坎公工会战',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # 是否可见
    enable_on_default=True,  # 是否默认启用
    bundle='娱乐',  # 属于哪一类
    help_=sv_help  # 帮助文本
)


@sv.on_fullmatch(["帮助-坎公工会战"])
async def helper(bot, ev):
    await bot.send(ev, sv_help)


#  会展报刀
@sv.on_fullmatch('报刀')
async def get_report(bot, ev):
    path = 'https://www.bigfun.cn/tools/gt/t_report'

    browser = await util.browser.get_browser()
    page = await browser.new_page(extra_http_headers=headers)
    await page.goto(path)
    await page.add_style_tag(content="body {max-width: 35.5rem;}")
    await page.add_style_tag(content=".banner-bottom {display: none;}")

    card = await page.query_selector(".t_report_top")
    assert card is not None
    img = await card.screenshot(type="png")
    await page.close()

    bio = io.BytesIO(img)
    base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()
    msg = f"[CQ:image,file={base64_str}]"
    await bot.send(ev, msg)


@sv.on_fullmatch('Boss状态')
async def get_boss_report(bot, ev):
    path = 'https://www.bigfun.cn/tools/gt/boss'

    browser = await util.browser.get_browser()
    page = await browser.new_page(extra_http_headers=headers)
    await page.goto(path)
    await page.add_style_tag(content=".banner-bottom {display: none;}")

    card = await page.query_selector(".boss_top")

    assert card is not None
    img = await card.screenshot(type="png")
    await page.close()

    bio = io.BytesIO(img)
    base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()
    msg = f"[CQ:image,file={base64_str}]"
    await bot.send(ev, msg)


@sv.on_fullmatch('总伤害统计')
async def count_damage(bot, ev):
    async with aiohttp.TCPConnector(verify_ssl=False) as connector:
        async with aiohttp.request(
                method='GET',
                url="https://www.bigfun.cn/api/feweb?target=kan-gong-guild-log-filter/a",
                connector=connector,
                headers=headers,
        ) as resp:
            res = await resp.json()
    print(res)

    data = res['data']
    date = data['date']
    member = data['member']
    total = {}
    for day in date:
        async with aiohttp.TCPConnector(verify_ssl=False) as connector:
            async with aiohttp.request(
                    method='GET',
                    url="https://www.bigfun.cn/api/feweb?target=kan-gong-guild-report/a&date=" + day,
                    connector=connector,
                    headers=headers,
            ) as resp:
                res = await resp.json()
        report = res['data']
        for item in report:
            total[item['user_id']] = item['damage_total']

    damageTotal = []
    for user in member:
        damage = 0
        if user['id'] in total:
            damage = total[user['id']]

        user['damage'] = damage
        damageTotal.append(user)

    damageTotal.sort(key=lambda k: (k.get('damage', 0)), reverse=True)

    msg = f'\t总伤害排行\n'
    for damageItem in damageTotal:
        msg += f"{damageItem['damage']} --【{damageItem['name']}】\n"
    await bot.send(ev, msg)
