from hoshino.config import DATA_DIR
from tortoise import Tortoise
import sqlite3

from nonebot.log import logger


async def db_init():
    logger.debug("开始连接数据库")
    try:
        await Tortoise.init(
            {
                "connections": {
                    "data": {
                        "engine": "tortoise.backends.sqlite",
                        "credentials": {"file_path": f"{DATA_DIR}data.db"},
                    },
                    "illust": {
                        "engine": "tortoise.backends.sqlite",
                        "credentials": {"file_path": f"{DATA_DIR}illust.db"},
                    },
                },
                "apps": {
                    "datadb": {
                        "models": ["hoshino.server.db.model.models"],
                        "default_connection": "data",
                    },
                    "illustdb": {
                        "models": ["hoshino.server.db.model.illust_model"],
                        "default_connection": "illust",
                    },
                },
            }
        )
        # await Tortoise.init(
        #     db_url=f"sqlite://{DATA_PATH}data.db",
        #     modules={"models": ["service.db.model.models"]},
        # )
        # await Tortoise.generate_schemas()
        # await Tortoise.init(
        #     db_url=f"sqlite://{DATA_PATH}illust.db",
        #     modules={"models": ["service.db.model.illust_model"]},
        # )
        await Tortoise.generate_schemas()
        logger.info("数据库连接成功")
    except:
        logger.warning("数据库连接失败，请尝试删除data目录下的data.db文件")


async def db_disconnect():
    await Tortoise.close_connections()
