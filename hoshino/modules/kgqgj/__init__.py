# -*- coding: utf-8 -*-
import base64
import io

from hoshino import Service, priv, util

sv_help = '''
- [坎公工会战]
- 报刀 - 当日会战报表
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
async def help_cos_v2(bot, ev):
    await bot.send(ev, sv_help)


#  会展报刀
@sv.on_fullmatch('报刀')
async def get_report(bot, ev):
    path = 'https://www.bigfun.cn/tools/gt/t_report'

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
