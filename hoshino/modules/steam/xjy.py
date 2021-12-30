from bs4 import BeautifulSoup as bs
from requests import get
from .util import Util

head = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 \
    (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36"}


def xjy_compare():
    xjy_url = "https://www.ithome.com/tag/xijiayi"
    xjy_page = get(url=xjy_url, headers=head).text
    soup = bs(xjy_page, "lxml")
    url_new = []
    for xjy_info in soup.find_all(name="a", class_="title"):
        info_soup = bs(str(xjy_info), "lxml")
        url_new.append(info_soup.a["href"])
    if not url_new:
        return "Server Error"
    else:
        url_old = []
        if Util.existsFile('xjy_result.json'):
            url_old = Util.readFile('xjy_result.json')
        seta = set(url_new)
        setb = set(url_old)
        compare_list = list(seta - setb)
    total = list(dict.fromkeys(url_new + url_old))
    Util.saveFile(total, 'xjy_result.json')
    return compare_list


def xjy_result(model, compare_list):
    result_text_list = []
    xjy_list = []
    if model == "Default":
        xjy_list = compare_list
    elif model == "Query":
        lines_list = Util.readFile('xjy_result.json')
        for i in lines_list:
            xjy_list.append(i.strip())
            if lines_list.index(i) == compare_list - 1:
                break
    try:
        for urls in xjy_list:
            page = get(url=urls, headers=head).text
            soup = bs(page, "lxml")
            title = bs(str(soup.find(name="h1")), "lxml").text

            info_soup = bs(str(soup.find(name="div", class_="post_content")), "lxml").find_all(name="p")
            second_text = ""
            for i in info_soup:
                if i.a is not None:
                    if i.a['href'] == "https://www.ithome.com/":
                        text = i.text + "|"
                    elif i.a.get('class') == 's_tag':
                        text = ""
                    else:
                        text = i.a["href"] + "|"
                    first_text = text
                else:
                    first_text = i.text + "|"
                second_text += first_text.replace("\xa0", " ")
            third_text = second_text.split("|")
            url_text = "未检测到领取地址"
            for part in third_text:
                if "http" in part:
                    url_text += "领取地址:" + part + "\n"
            if url_text == '未检测到领取地址':
                continue
            final_text = f"{title}\n{url_text.replace('未检测到领取地址', '')}"
            result_text_list.append(final_text)
    except Exception as e:
        result_text_list = f"error:{e}"
    return result_text_list
