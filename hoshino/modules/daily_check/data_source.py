import time
import httpx
import random
from hoshino import util, config
import json

fortune: list[dict]
msg_of_day: list[dict]
atri_text: list[dict]

with open(f"{config.TEXT_PATH}fortune.json", "r", encoding="utf-8") as file:
    fortune = json.load(file)["data"]

with open(f"{config.TEXT_PATH}msg_of_day.json", "r", encoding="utf-8") as file:
    msg_of_day = json.load(file)["data"]


async def get_acg_image():
    url = "https://v2.alapi.cn/api/acg"
    params = {"token": config.ALAPI_TOKEN, "format": "json"}
    async with httpx.AsyncClient(headers=util.browser.get_ua()) as client:
        resp = await client.get(url=url, params=params)
    try:
        return resp.json()["data"]["url"]
    except:
        return "https://file.alapi.cn/image/comic/122514-15234207140623.jpg"


async def get_stick(user_id: int):
    time_day = time.strftime("%Y%m%d", time.localtime())
    seed = int(str(user_id) + str(time_day))
    random.seed(seed)
    result = random.choice(fortune)
    if "吉" not in result["FORTUNE_SUMMARY"]:
        seed = seed + 15
        result = random.choice(fortune)
    return result


async def get_msg(user_id: int):
    time_day = time.strftime("%Y%m%d", time.localtime())
    seed = int(str(user_id) + str(time_day))
    random.seed(seed)
    result = random.choice(msg_of_day)
    return result


async def get_greet():
    hour = int(time.strftime("%H", time.localtime()))
    if hour in range(0, 6):
        return f"凌晨好"
    if hour in range(6, 12):
        return f"早上好"
    if hour in range(12, 18):
        return f"下午好"
    if hour in range(18, 25):
        return f"晚上好"
    return f""
