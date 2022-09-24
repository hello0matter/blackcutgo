# coding=utf-8
import os
import sys
sys.path.insert(1, '../')
import blackgo.timetask as timetask
import argparse
import json
import requests
import urllib3

urllib3.disable_warnings()
from datetime import datetime


class Logger(object):
    def __init__(self, filename=sys.path[0] + '/' + str(datetime.now()).replace(" ", "").replace("-", "").replace(":",
                                                                                                                  "") + 'out.log',
                 stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


sys.stdout = Logger(stream=sys.stdout)  # 将控制台输出保存到文件中


class JsonRead:
    def __init__(self, d):
        self.__dict__ = d


def post(**arg):
    arg = arg['arg']
    url = 'https://services.mojing1.com/api/Mall/list?page=1&limit=10&sort=price%2Ctime&order=desc%2Cdesc&keywords=&id&isMystery=0&rights=-1&level'
    headers = {'Host': 'services.mojing1.com', 'Connection': 'keep-alive',
               'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
               'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjYwOTIzMTAsImlhdCI6MTY2MzUwMDMxMCwidXNlcklkIjoiNzA2MzQifQ.QSOxQe-vlvmjc87HaDqBDlX-XWoJMwBRpFme_1fsVeo',
               'sec-ch-ua-mobile': '?0',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
               'sec-ch-ua-platform': '"Windows"', 'Accept': '*/*', 'Origin': 'https://app.mojing1.com',
               'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
               'Referer': 'https://app.mojing1.com/', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6'}
    cookies = {}
    data = {}

    html = requests.get(url, headers=headers, verify=False, cookies=cookies)
    print(len(html.text))
    print(html.text)


parser = argparse.ArgumentParser()

# 在参数构造器中添加两个命令行参数
parser.add_argument('--time', type=str, default='')
parser.add_argument('--type', type=int, default=1)
parser.add_argument('--desc', type=str, default='')

# 获取所有的命令行参数
args = parser.parse_args()
with open(sys.path[0] + '/account.txt', 'r', encoding='utf-8') as f:
    read_data = f.readlines()
    if args.desc:
        print(args.desc, "账号数量", len(read_data))

    for item in read_data:
        txt = item.split("----")
        print(txt)

    with open(sys.path[0] + '/conf.json', 'r', encoding='utf-8') as f:
        jsonStr = f.read()
        config = json.loads(jsonStr, object_hook=JsonRead)

        print("线程数", config.thread)
        list = [[1], [2]]
        for x in range(config.thread):
            arr = list[x]
            timetask.buy_monitor(args.time, post, "hulianar" + str(x), dict(arg=arr)) if args.time else print(
                "未设置执行时间") / exit()

        input()
