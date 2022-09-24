import sys
from urllib import parse
import requests
from datetime import datetime


# 无限重发
def repeats():
    with open(sys.path[0] + '/' + str(datetime.now()).replace(" ", "").replace("-", "").replace(":", "") + 'out.txt',
              'a+', encoding='utf-8') as f:
        test = [1, 2, 3, 4]
        for i in range(100):
            url = 'https://api.innskins.com/pat/admin/v1/user'
            headers = {'Host': 'api.innskins.com', 'Connection': 'keep-alive', 'Content-Length': '112',
                       'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
                       'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
                       'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json;charset=UTF-8',
                       'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyYjU2MzU5ZTExYTI4MDA1NTU3YjQ0YSIsImlhdCI6MTY2MzkxODkyNSwiZXhwIjoxNjYzOTYyMTI1fQ.mgBpKBbDQCFWNTme2IxXECjzdM_fEsZfUsiNRbT_Z4ZILZSwP0cpAyfxOMzZXHkWqjU2Mm1-h7cjfXg9x_h6HRFy5QaX8ZsSfnfhRVcmVOAJJpNiRX_bQ1y474t-3KK2NwOtcL_7gnyfSNIETOMuUrp09cjoF1VjxwguANeXLH4',
                       'sec-ch-ua-mobile': '?0',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
                       'sec-ch-ua-platform': '"Windows"', 'Origin': 'https://amp.innskins.com',
                       'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
                       'Referer': 'https://amp.innskins.com/', 'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6'}
            cookies = {}
            data = '{"type":1,"sex":1,"origin":0,"channel":1,"nickname":"12","email":"122323@qq.com","password":"122323","status":1}'

            html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data,
                                 proxies={'https': 'http://127.0.0.1:8888'})
            print(len(html.text))
            print(html.text)
            # print(html.text.decode(''))
            f.writelines(html.text)


# 读文件重发
def open_txt():
    with open(sys.path[0] + '/test.txt', 'r', encoding='utf-8') as f:
        read_data = f.readlines()
        for i in range(len(read_data)):
            line = read_data[i].strip()
            txt = parse.quote(line, 'utf-8')
            url = 'http://zjfjdc.zjjt365.com:5002/hz_mysql_api/BatteryBinding/checkCjhDc?token=0571_2c2df305-38b4-4b62-99fd-31e2e02cf932&city=0571&cjhurl=http%3A%2F%2Fwww.pzcode.cn%2Fvin%2F140522209851110&dcbhurl=' + txt
            headers = {'Host': 'zjfjdc.zjjt365.com:5002', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'}
            cookies = {'SERVERID': '941743a4a2850041e1e7cef946493742|1663769338|1663759342'}
            data = {}

            html = requests.get(url, headers=headers, verify=False, cookies=cookies)
            print(html.text)


# 读文件切割重发
def open_txt2():
    with open(sys.path[0] + '/test2.txt', 'r', encoding='utf-8') as f:
        read_data = f.readlines()
        for i in range(len(read_data)):
            line = read_data[i].strip()
            txt2 = line.split("----")
            url = 'https://api.innskins.com/pat/admin/v1/user'
            headers = {'Host': 'api.innskins.com', 'Connection': 'keep-alive', 'Content-Length': '112',
                       'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
                       'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
                       'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json;charset=UTF-8',
                       'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyYjU2MzU5ZTExYTI4MDA1NTU3YjQ0YSIsImlhdCI6MTY2MzkxODkyNSwiZXhwIjoxNjYzOTYyMTI1fQ.mgBpKBbDQCFWNTme2IxXECjzdM_fEsZfUsiNRbT_Z4ZILZSwP0cpAyfxOMzZXHkWqjU2Mm1-h7cjfXg9x_h6HRFy5QaX8ZsSfnfhRVcmVOAJJpNiRX_bQ1y474t-3KK2NwOtcL_7gnyfSNIETOMuUrp09cjoF1VjxwguANeXLH4',
                       'sec-ch-ua-mobile': '?0',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
                       'sec-ch-ua-platform': '"Windows"', 'Origin': 'https://amp.innskins.com',
                       'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
                       'Referer': 'https://amp.innskins.com/', 'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6'}
            cookies = {}
            data = '{"type":1,"sex":1,"origin":0,"channel":1,"nickname":"' + txt2[0] + '","email":"' + txt2[
                1] + '","password":"' + txt2[2] + '","status":1}'
            html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data,
                                 proxies={'https': 'http://127.0.0.1:8888'})
            print(len(html.text))
            print(html.text)


open_txt2()
# repeats()
