# -*- coding: utf-8 -*-
import aiohttp
import base64
import io

from hoshino import Service, priv, util
from .data_source import get_member, get_boss_info, today_report, headers

sv_help = '''
- [坎公工会战]
- 报刀 - 当日会战报表
- boss状态 - Boss状态
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
    await page.wait_for_timeout(100)
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


@sv.on_fullmatch(('Boss状态', 'boss状态', 'BOSS状态'))
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


@sv.on_fullmatch('总伤统计')
async def count_damage(bot, ev):
    async with aiohttp.TCPConnector(verify_ssl=False) as connector:
        async with aiohttp.request(
                method='GET',
                url="https://www.bigfun.cn/api/feweb?target=kan-gong-guild-log-filter/a",
                connector=connector,
                headers=headers,
        ) as resp:
            res = await resp.json()

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
            if item['user_id'] in total:
                total[item['user_id']] += item['damage_total']
            else:
                total[item['user_id']] = 0

    damageTotal = []
    for user in member:
        damage = 0
        if user['id'] in total:
            damage = total[user['id']]

        user['damage'] = damage
        damageTotal.append(user)

    damageTotal.sort(key=lambda k: (k.get('damage', 0)), reverse=True)

    msg = f'\t总伤害排行\n'
    i = 0
    for damageItem in damageTotal:
        i = i + 1
        msg += f"{i}\t{damageItem['damage']} --【{damageItem['name']}】\n"
    await bot.send(ev, msg)


@sv.on_fullmatch('出刀状态')
async def damage_status(bot, ev):
    # 先获取用户
    member = await get_member()
    # 再获取报表
    report = await today_report()

    reportMap = {}
    for item in report:
        reportMap[item['user_id']] = item

    dataList = []
    for user in member:
        uid = user['id']
        name = user['name']
        damage_num = 0
        damage_total = 0
        if uid in reportMap:
            damage_num = reportMap[uid]['damage_num']
            damage_total = reportMap[uid]['damage_total']

        dataItem = {
            'name': name,
            'damage_num': damage_num,
            'damage_total': damage_total,
        }
        dataList.append(dataItem)
    # 将dataList按damage_num排序 从高到低
    dataList.sort(key=lambda k: (k.get('damage_num', 0)), reverse=True)
    msg = f'==== 出刀状态 ====\n'
    for damageItem in dataList:
        msg += f"{damageItem['damage_num']}刀 -- \t {damageItem['damage_total']}伤害 -- \t {damageItem['name']}\n"
    await bot.send(ev, msg)


@sv.on_fullmatch('出刀详细')
async def DamageDetail(bot, ev):
    HTML_code = """
      <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
        <style>
            html,
            body {
                margin: 0;
                height: 100%;
                display: flex;
                justify-content: center;
                background-color: #f5f5f5;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                border: 1px solid #ccc;
                padding: 1rem 1rem 1rem 1rem;
                min-height: 350px;
                box-shadow: 0 8px 60px -10px rgba(13, 28, 39, 0.6);
                background: #fff;
                border-radius: 16px;
                max-width: 700px;
                position: relative;
            }

            th, td {
                border: 1px solid #000;
                padding: 0.5rem 0.5rem 0.5rem 0.5rem;
                text-align: center;
            }

            th {
                background: #f5f5f5;
            }
        </style>
    </head>
    <body>
    <table>
        <thead>
        <tr>
            <th>成员</th>
            <th>出刀</th>
            <th>伤害</th>
            <th>boos1</th>
            <th>boos2</th>
            <th>boos3</th>
            <th>boos4</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>1</td>
            <td>1</td>
            <td>2</td>
            <td>3</td>
            <td>4</td>
            <td>5</td>
            <td>6</td>
        </tr>
        </tbody>
    </table>

    </body>
    </html>
        """
    boss = await data_source.get_boss_info()
    bossMap = {}
    for item in boss:
        bossMap[item['id']] = item

    # 先获取用户
    member = await get_member()
    # 再获取报表
    report = await today_report()

    reportMap = {}
    for item in report:
        reportMap[item['user_id']] = item

    msg = f'==== 出刀状态 ====\n'
    for user in member:
        uid = user['id']
        name = user['name']
        damage_num = 0
        damage_total = 0
        if uid in reportMap:
            damage_num = reportMap[uid]['damage_num']
            damage_total = reportMap[uid]['damage_total']
            damage_list = reportMap[uid]['damage_list']
            # 详情
            for damage in damage_list:
                # damage['damage'] # 伤害
                # damage['boss_name'] # 伤害类型
                msg += f"{damage['damage']} --【{damage['name']}】\n"

    await bot.send(ev, msg)


def getBossTable(boss):
    table = f'<table><thead><tr><th>BOSS</th><th>Lv</th><th>属性</th><th>总生命值</th><th>剩余生命值</th></tr></thead><tbody>'
    for item in boss:
        table += f'<tr>'
        table += f'<td>{item["name"]}</td>'
        table += f'<td>{item["level"]}</td>'
        table += f'<td>{item["elemental_type_cn"]}</td>'
        table += f'<td>{item["total_hp"]}</td>'
        table += f'<td>{item["remain_hp"]}</td>'
        table += f'</tr>'

    table += f'</tbody></table>'
    return table
