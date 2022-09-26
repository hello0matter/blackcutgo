# coding=utf-8
import atexit
import os
import sys
import threading
import hashlib
from urllib import parse

import requests
from PySide6.QtCore import QSettings
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
import rc_obj
import json



def main__login__thread(usercode, password, city):
    global window, settings, token__data
    try:
        md5s = hashlib.md5()
        md5s.update(password.encode('utf8'))
        hexdigest = md5s.hexdigest()
        url = 'http://zjfjdc.zjjt365.com:5002/hz_mysql_api/BatteryBinding/login?usercode=' + usercode + '&password=' + hexdigest + '&city=' + city
        # headers = {'Host': 'zjfjdc.zjjt365.com:5002', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'}
        # cookies = {'SERVERID': '941743a4a2850041e1e7cef946493742|1664087759|1664087489'}
        # data = {}
        # url = 'http://zjfjdc.zjjt365.com:5002/hz_mysql_api/BatteryBinding/login?usercode=1&password=c4ca4238a0b923820dcc509a6f75849b&city=0573'
        headers = {'Host': 'zjfjdc.zjjt365.com:5002', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip',
                   'User-Agent': 'okhttp/4.9.1'}
        cookies = {}
        data = {}

        html = requests.get(url, headers=headers, verify=False, cookies=cookies)
        token__data = json.loads(html.text)['data']

        if token__data:
            window.setProperty('loginData', token__data)
            settings.setValue("loginData", token__data)
        else:
            window.setProperty('loginData', "")
    except Exception as e:
        print(e)
    window.setProperty('isUpdating', False)



def cr__code():
    with open(sys.path[0] + '/test.txt', 'r', encoding='utf-8') as f:
        read_data = f.readlines()
        for i in range(len(read_data)):
            line = read_data[i].strip()
            txt = parse.quote(line, 'utf-8')
            url = 'http://zjfjdc.zjjt365.com:5002/hz_mysql_api/BatteryBinding/checkCjhDc?token=' + token__data + '&city=0571&cjhurl=http%3A%2F%2Fwww.pzcode.cn%2Fvin%2F140522209851110&dcbhurl=' + txt
            headers = {'Host': 'zjfjdc.zjjt365.com:5002', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'}
            cookies = {'SERVERID': '941743a4a2850041e1e7cef946493742|1663769338|1663759342'}
            data = {}

            html = requests.get(url, headers=headers, verify=False, cookies=cookies)
            msg = json.loads(html.text)['msg']



def main__login(usercode, password, city):
    task = threading.Thread(target=main__login__thread, args=(usercode, password, city))
    task.start()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    #    engine.addImportPath("qrc:/")
    # qml_file = Path(__file__).resolve().parent / "main.qml"

    #    qml_file = "main.qml"
    engine.load(":/obj/main.qml")
    engine.load(":/obj/ToastManager.qml")
    engine.load(":/obj/Toast.qml")
    # 获取 root 对象.
    window = engine.rootObjects()[0]
    window.main__login.connect(main__login)
    settings = QSettings("config.ini", QSettings.IniFormat)
    # settings = QSettings("config.ini", QSettings.IniFormat)
    token__data = settings.value("loginData")
    if os.path.isfile("rc_obj.py"):
        os.remove("rc_obj.py")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
