import re
from hoshino import Service, priv
from .data_source import get_chat_result

try:
    import ujson as json
except ImportError:
    import json

sv_help = '''
[@bot XX] @bot就可以与bot对话
'''.strip()

sv = Service(
    name='人工智障',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=True,  # 是否默认启用
    bundle='通用',  # 属于哪一类
    help_=sv_help  # 帮助文本
)


@sv.on_fullmatch(["帮助-人工智障"])
async def helper(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)


cq_code_pattern = re.compile(r'\[CQ:\w+,.+\]')


@sv.on_message('group')
async def ai_reply(bot, ev):
    msg = str(ev['message'])

    if not msg.startswith(f'[CQ:at,qq={ev["self_id"]}]'):
        return

    text = re.sub(cq_code_pattern, '', msg).strip()
    if text == '':
        return
    replay = await get_chat_result(text, ev['user_id'])

    await bot.send(ev, replay, at_sender=True)
