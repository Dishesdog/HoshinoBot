import hoshino
import asyncio
from hoshino.server.init import init_bot

bot = hoshino.init()
app = bot.asgi

bot.on_startup(init_bot)

if __name__ == '__main__':
    bot.run(use_reloader=False, loop=asyncio.get_event_loop())
