from aiohttp.client import ClientSession
import aiohttp
import random
from hoshino import config

try:
    import ujson as json
except ImportError:
    import json

url = "http://openapi.tuling123.com/openapi/api/v2"

check_url = "https://v2.alapi.cn/api/censor/text"

index = 0

DATA_PATH = config.DATA_DIR

anime_data = json.load(open(DATA_PATH + "anime.json", "r", encoding="utf8"))


# 图灵AI
async def get_chat_result(text: str, user_id: int) -> str:
    #  回复字典
    if text in anime_data.keys():
        return random.choice(anime_data[text])

    # 图灵
    async with aiohttp.ClientSession() as sess:
        rst = await tu_ling(text, user_id, sess)
        # if not rst:
        # rst = await xie_ai(text, sess)
    if not rst:
        return no_result()
    return rst


# 图灵接口
async def tu_ling(text: str, user_id: int, sess: ClientSession):
    apiKey = random.choice(config.TL_KEY)
    req = {
        "perception": {
            "inputText": {"text": text},
            "selfInfo": {
                "location": {"city": "陨石坑", "province": "火星", "street": "第5坑位"}
            },
        },
        "userInfo": {"apiKey": apiKey, "userId": str(user_id)},
    }
    text = ""
    async with sess.post(url, json=req) as response:
        if response.status != 200:
            return no_result()
        resp_payload = json.loads(await response.text())
        if int(resp_payload["intent"]["code"]) in [4003]:
            return ""
        if resp_payload["results"]:
            for result in resp_payload["results"]:
                if result["resultType"] == "text":
                    text = result["values"]["text"]
                    if "请求次数超过" in text:
                        text = ""
    return text


#
#
# # 屑 AI
# async def xie_ai(text: str, sess: ClientSession):
#     async with sess.get(
#             f"http://api.qingyunke.com/api.php?key=free&appid=0&msg={text}"
#     ) as res:
#         content = ""
#         data = json.loads(await res.text())
#         if data["result"] == 0:
#             content = data["content"]
#             if "菲菲" in content:
#                 content = content.replace("菲菲", f"{NICKNAME}")
#             if "公众号" in content:
#                 content = ""
#             if "{br}" in content:
#                 content = content.replace("{br}", "\n")
#             if "提示" in content:
#                 content = content[: content.find("提示")]
#             if "淘宝" in content:
#                 return ""
#             while True:
#                 r = re.search("{face:(.*)}", content)
#                 if r:
#                     id_ = r.group(1)
#                     content = content.replace(
#                         "{" + f"face:{id_}" + "}", str(face(int(id_)))
#                     )
#                 else:
#                     break
#         return content if not content and not ALAPI_AI_CHECK else await check_text(content, sess)

#
# # 打招呼内容
# def hello() -> str:
#     result = random.choice(
#         (
#             "哦豁？！",
#             "你好！Ov<",
#             f"库库库，呼唤{list(get_bot().config.nickname)[0]}做什么呢",
#             "我在呢！",
#             "呼呼，叫俺干嘛",
#         )
#     )
#     img = random.choice(os.listdir(IMAGE_PATH + "zai/"))
#     if img[-4:] == ".gif":
#         result += image(img, "zai")
#     else:
#         result += image(img, "zai")
#     return result


# 没有回答时回复内容
def no_result() -> str:
    return (
        random.choice(
            [
                "你在说啥子？",
                f"纯洁的我没听懂",
                "下次再告诉你(下次一定)",
                "你觉得我听懂了吗？嗯？",
                "我！不！知！道！",
                '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
                '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
                '其实我不太明白你的意思……',
                '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～',
                '唔……等会再告诉你'
            ]
        )
        # + image(random.choice(os.listdir(IMAGE_PATH + "noresult/")), "noresult")
    )


#
# # 检测屑AI回复的文本是否是 *话
# async def check_text(text: str, sess: ClientSession) -> str:
#     if not ALAPI_TOKEN:
#         return text
#     params = {"token": ALAPI_TOKEN, "text": text}
#     try:
#         async with sess.get(check_url, timeout=2, params=params) as response:
#             data = await response.json()
#             if data["code"] == 200:
#                 if data["conclusion_type"] == 2:
#                     return ''
#     except Exception as e:
#         logger.error(f"检测违规文本错误...e：{e}")
#     return text


if __name__ == "__main__":
    pass
