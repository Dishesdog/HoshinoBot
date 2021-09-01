# from utils.data import load_data
from hoshino.server.db.database_sqlite import db_init
from hoshino.util.browser import install


async def init_bot():
    # 建立数据库连接
    await db_init()

    # 检查更新Playwright的Chromuim
    await install()
