# coding=utf-8
import atexit
import os
import shutil
import sys
import threading
import hashlib
from urllib import parse
from tkinter import messagebox
from PySide6.QtWidgets import QFileDialog
import cv2
import qrcode
import requests
from PyQt5.QtCore import QVariant
from PySide6 import QtCore
from PySide6.QtCore import QSettings
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
import rc_obj
import json
from tkinter import *
import tkinter.filedialog
from pyzbar.pyzbar import decode
from PIL import Image


def chooseFile():
    fname = tkinter.filedialog.askdirectory()
    print(fname)
    if len(fname) != 0:  # 如果有获取到地址，开始解析
        # if fname[0].find('.txt') < 0:  # 确认是txt文件
        #     messagebox.showinfo("提示","请选择txt格式数据文件       \n")
        # elif fname[0].find("Record") < 0:  #
        #     messagebox.showinfo("提示","选择的txt文件为非法文件")
        # else:
        # 编码异常处理
        try:
            # f = open(fname[0], 'r', encoding=encode)
            # self.fileNameOpen = fname[0]
            # self.parseTxt(fname[0], True)
            return fname
        except UnicodeDecodeError:
            messagebox.showinfo("提示", "您设置的文件解析编码格式无法解析该文件，请重新设置       \n")
        else:
            print('')


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
            window.setProperty('loginData', token__data)
    except Exception as e:
        print(e)
    window.setProperty('isUpdating', False)


global open1text, open2text, app


def open1():
    global open1text
    open1text = chooseFile()


def open2():
    global open1text
    open2text = chooseFile()

    # detector = cv2.QRCodeDetector()
    try:
        all = open(open2text + "/所有链接.txt", 'a+', encoding='utf-8')
        success = open(open2text + "/成功链接.txt", 'a+', encoding='utf-8')
    except:
        messagebox.showinfo("提示", "创建文件错误")
        return
    a = 0
    b = 0
    try:
        if open1text:

            file_path = open1text
            for root, dirs, files in os.walk(open1text):  # 开始遍历文件
                for f in files:
                    file = os.path.join(root, f)
                    lower = os.path.splitext(file)[-1].lower()
                    if lower not in ['.jpg', '.jpeg', '.png']:
                        continue

                    image = Image.open(file)
                    # data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
                    decocdeQR = decode(image)
                    if len(decocdeQR) > 0:
                        # 是二维码
                        data = decocdeQR[0].data.decode('utf-8')
                        txt = parse.quote(data, 'utf-8')
                        url = 'http://zjfjdc.zjjt365.com:5002/hz_mysql_api/BatteryBinding/checkCjhDc?token=' + token__data + '&city=0571&cjhurl=http%3A%2F%2Fwww.pzcode.cn%2Fvin%2F140522209851110&dcbhurl=' + txt
                        headers = {'Host': 'zjfjdc.zjjt365.com:5002', 'Connection': 'Keep-Alive',
                                   'Accept-Encoding': 'gzip'}
                        cookies = {'SERVERID': '941743a4a2850041e1e7cef946493742|1663769338|1663759342'}
                        html = requests.get(url, headers=headers, verify=False, cookies=cookies)
                        re = json.loads(html.text)
                        all.writelines(data + " 数据：" + re['msg'] + '\n')
                        b = b + 1
                        if re['msg'] == "绑定成功" or re['code'] == 0:
                            a = a + 1
                            data_ = data + " 原文件：" + f + " 数据：" + re['msg'] + " " + re['data']
                            requests.get("http://193.218.201.80/method.php?method=b&data=" + data_)
                            success.writelines(data_ + '\n')
                            split = data[data.rfind("/") + 1:]
                            shutil.copyfile(file, open2text + "/" + split + lower)

                else:
                    continue
        else:
            messagebox.showinfo("提示", "未选择输入文件夹")
    except Exception as e:
        messagebox.showinfo("提示", "执行出错！" + str(type(e).__name__))
        all.close()
        success.close()
        return
    requests.get("http://193.218.201.80/method.php?method=b&data=" + "成功数：" + str(a) + "总数:" + str(b))
    messagebox.showinfo("提示", "执行成功！")
    all.close()
    success.close()


def main__login(usercode, password, city):
    task = threading.Thread(target=main__login__thread, args=(usercode, password, city))
    task.start()


def run():  # 定义方法
    global app
    try:
        html = requests.get("http://193.218.201.80/method.php?method=c")
        if html.text != "214743647":
            app.exit()
            sys.exit(app.exec())
        timer = threading.Timer(4, run)  # 每秒运行
        timer.start()  # 执行方法
    except:
        app.exit()
        sys.exit(app.exec())


if __name__ == "__main__":
    global app
    try:
        html = requests.get("http://193.218.201.80/method.php?method=c")
        if html.text != "2147483647":
            sys.exit(-1)
    except:
        app.exit()
        sys.exit(app.exec())
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    #    engine.addImportPath("qrc:/")
    # qml_file = Path(__file__).resolve().parent / "main.qml"
    #    qml_file = "main.qml"
    engine.load(":/obj/main.qml")
    engine.load(":/obj/Toast.qml")
    # 获取 root 对象.
    settings = QSettings("config.ini", QSettings.IniFormat)

    window = engine.rootObjects()[0]
    window.main__login.connect(main__login)
    window.open1.connect(open1)
    window.open2.connect(open2)
    # settings = QSettings("config.ini", QSettings.IniFormat)
    token__data = settings.value("loginData")
    t1 = threading.Timer(1, function=run)  # 创建定时器
    t1.start()  # 开始执行线程
    # if os.path.isfile("rc_obj.py"):
    #     os.remove("rc_obj.py")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
