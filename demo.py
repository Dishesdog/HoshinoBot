import re

import requests
import os
import time


def main():
    url = 'https://m.douyu.com/5931314'
    text = requests.get(url).text
    for i in text.split("\n"):
        regex = re.compile(r"var \$ROOM = ([^']*)")
        match = regex.search(i)
        if match:
            res = dict(eval(match.group(1)))
            return res
    return None


if __name__ == "__main__":
    a = main()
    print(a)