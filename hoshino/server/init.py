from hoshino.server.db.database_sqlite import db_init
from hoshino.util.browser import close_browser


async def init_bot():
    # 建立数据库连接
    await db_init()
