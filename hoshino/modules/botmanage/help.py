from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service(name='_help_', manage_priv=priv.SUPERUSER, visible=False)

TOP_MANUAL = '''
※群管理可控制开关功能※
[lssv] 查看模块的开关状态
[启用+空格+service]
[禁用+空格+service]
=====================
※bot开源项目：
github.com/Ice-Cirno/HoshinoBot
※您的支持是本bot更新维护的动力
'''.strip()


def gen_bundle_manual(bundle_name, service_list, gid):
    manual = [bundle_name]
    service_list = sorted(service_list, key=lambda s: s.name)
    for sv in service_list:
        if sv.visible:
            spit_line = '=' * max(0, 18 - len(sv.name))
            manual.append(f"|{'○' if sv.check_enabled(gid) else '×'}| {sv.name} {spit_line}")
            if sv.help:
                manual.append(sv.help)
    return '\n'.join(manual)


@sv.on_prefix('help', '帮助')
async def send_help(bot, ev: CQEvent):
    bundle_name = ev.message.extract_plain_text().strip()
    bundles = Service.get_bundles()
    if not bundle_name:
        await bot.send(ev, TOP_MANUAL)
    elif bundle_name in bundles:
        msg = gen_bundle_manual(bundle_name, bundles[bundle_name], ev.group_id)
        await bot.send(ev, msg)
    # else: ignore
