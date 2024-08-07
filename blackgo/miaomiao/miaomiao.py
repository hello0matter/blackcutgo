# coding=utf-8
import sys
sys.path.insert(1, '../')
import importlib
# 使用 import_module 导入模块并确保只导入一次
timetask = importlib.import_module('timetask')
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
    # arg = arg['arg']
    url = 'https://miaomiao.scmttec.com/seckill/seckill/subscribe.do'
    headers = {'Host': 'miaomiao.scmttec.com', 'Content-Length': '61', 'Tk': 'wxapptoken:10:95b585e58c5badaa9353ce5db0e7eebd_1d5d715877b03277e4b3ca936613be35', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Accept': 'application/json, text/plain, */*', 'Ecc-Hs': 'fee87e30abad5a013a681c4d58314475', 'Xweb_xhr': '1', 'X-Requested-With': 'XMLHttpRequest', 'Isformdata': '[object Boolean]', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://servicewechat.com/wxff8cad2e9bf18719/36/page-frame.html', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-us,en'}
    cookies = {'_xxhm_': '%7B%22id%22%3A38385879%2C%22mobile%22%3A%2217680492987%22%2C%22nickName%22%3A%22%E5%BE%AE%E4%BF%A1%E7%94%A8%E6%88%B7%22%2C%22headerImg%22%3A%22https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FPOgEwh4mIHO4nibH0KlMECNjjGxQUq24ZEaGT4poC6icRiccVGKSyXwibcPq4BWmiaIGuG1icwxaQX6grC9VemZoJ8rg%2F132%22%2C%22regionCode%22%3A%22440304%22%2C%22name%22%3A%22*%E9%9B%84%22%2C%22birthday%22%3A%222000-01-12+02%3A00%3A00%22%2C%22sex%22%3A1%2C%22hasPassword%22%3Afalse%2C%22birthdayStr%22%3A%222000-01-12%22%7D', '_xzkj_': 'wxapptoken%3A10%3A95b585e58c5badaa9353ce5db0e7eebd_1d5d715877b03277e4b3ca936613be35', 'b0ae': '8b7b44768c60540a7e', 'b9cd': '29adccc0420d2bd769', 'fff8': '3ad6f66dac92596ae8', '218f': '690f8ab93c420a46e1', 'b6e3': 'f9831bb04763467108', '24c5': '1d2464faa836627745', '4485': '5ec0e2f005a791eacc', '9586': '506b0718a7bfb12eee', 'tgw_l7_route': '31e26ac7a066ca4fc11361525ae43d81'}
    data = {'seckillId': '5522', 'linkmanId': '37265861', 'idCardNo': '430521200107219308'}
    # #
    # # html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
    #
    # url = 'https://miaomiao.scmttec.com/seckill/linkman/findByUserId.do'
    # headers = {'Host': 'miaomiao.scmttec.com', 'Connection': 'keep-alive', 'charset': 'utf-8', 'tk': 'wxapptoken:10:95b585e58c5badaa9353ce5db0e7eebd_1e89cfba7fa90c0d33530619be9bb262', 'x-requested-with': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Linux; Android 13; RMX2202 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4425 MMWEBSDK/20221109 Mobile Safari/537.36 MMWEBID/8934 MicroMessenger/8.0.31.2280(0x28001F35) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64 MiniProgramEnv/android', 'content-type': 'application/json', 'Accept-Encoding': 'gzip,compress,br,deflate', 'accept': 'application/json, text/plain, */*', 'Referer': 'https://servicewechat.com/wxff8cad2e9bf18719/36/page-frame.html'}
    # cookies = {'_xzkj_': 'wxapptoken%3A10%3A95b585e58c5badaa9353ce5db0e7eebd_1e89cfba7fa90c0d33530619be9bb262', '_xxhm_': '%7B%22id%22%3A38385879%2C%22mobile%22%3A%2217680492987%22%2C%22nickName%22%3A%22%E5%BE%AE%E4%BF%A1%E7%94%A8%E6%88%B7%22%2C%22headerImg%22%3A%22https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FPOgEwh4mIHO4nibH0KlMECNjjGxQUq24ZEaGT4poC6icRiccVGKSyXwibcPq4BWmiaIGuG1icwxaQX6grC9VemZoJ8rg%2F132%22%2C%22regionCode%22%3A%22440304%22%2C%22name%22%3A%22*%E9%9B%84%22%2C%22birthday%22%3A%222000-01-12+02%3A00%3A00%22%2C%22sex%22%3A1%2C%22hasPassword%22%3Afalse%2C%22birthdayStr%22%3A%222000-01-12%22%7D', '077e': '109d80b83988c4cbcb', 'eb66': '6fd2d5c1b60a0f864d'}
    #
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
            timetask.buy_monitor(args.time, post, "miaomiao" + str(x), dict(arg=arr)) if args.time else print(
                "未设置执行时间") / exit()

        input()
