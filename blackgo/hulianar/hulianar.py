# coding=utf-8
import os
import sys
sys.path.insert(1, '../')
import blackgo.timetask as timetask
import argparse
import json


class JsonRead:
    def __init__(self, d):
        self.__dict__ = d


def post(exe, thread):
    print(1)
    os.popen(exe)


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
    f.closed

    # timetask.buy_monitor("* * * * * *", post, "hulianar")
    with open(sys.path[0] + '/conf.json', 'r', encoding='utf-8') as f:
        jsonStr = f.read()
        config = json.loads(jsonStr, object_hook=JsonRead)

        if "curl" in dir(config):
            this_cut = config.curl
            # 替换参数
            this_cut.replace('${1}', "")
            this_cut.replace('${2}', "")
        else:
            print("未设置curl语句")

        this_cut = """while true
        do
            """ + this_cut + """
        done"""

        print("线程数", config.thread, this_cut)

        for x in range(config.thread):
            # timetask.buy_monitor(args.time, post, "hulianar" + str(x)) if args.time else print("未设置执行时间") / exit()
            timetask.buy_monitor(args.time, post, "hulianar" + str(x), dict(exe=this_cut, thread=config.thread)) if args.time else print("未设置执行时间") / exit()

        # os.system("pause")
