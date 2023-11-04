# coding=utf-8
import ast
import hashlib
import json
import random
import shutil
import subprocess
import sys
import threading
import time
import tkinter.filedialog
from tkinter import Tk
from urllib import parse

import pyautogui
import qrcode
import requests
from PySide6.QtCore import QSettings
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from pyzbar.pyzbar import decode

import os
from pathlib import Path
from typing import Optional, Tuple, Union

from PIL import Image, ImageDraw, ImageFont  # pip install pillow
import rc_obj

# dc	x	ewm	dcl	ewml tnl
# 全局参数
global open1text, open2text, app, codes, open3txt, times, settings, open4text, open5text, tnl, tnl2, thisa, thisb, ab, thisc
thisc = '1'
tnl = 0
tnl2 = 1
thisa = 0
thisb = 0
open5text = ''
ab = []
# 获取图片宽度
def get_img_width(fname) -> int:
    return Image.open(fname).size[0]


# 获取图片高度
def get_img_height(fname) -> int:
    return Image.open(fname).size[1]


# 给图片加文字
# 生成blank_img空白图片，加上文字之后生成新图片或覆盖旧图, 宽度为origin_img原始图片的宽度

MARGIN_LEFT, MARGIN_TOP = 40, 10
FONT_SIZE = 12
FONT_COLOR = "black"


def gen_text_img(
        origin_img: Union[Path, str],
        text: str,
        img_path=None,
        color=FONT_COLOR,
        font_size: int = FONT_SIZE,
        margin_left: int = MARGIN_LEFT,
        margin_top: int = MARGIN_TOP,
        blank_img=None,
        font_path: Optional[str] = None,
        show_img: bool = False,
) -> Union[Path, str]:
    width = get_img_width(origin_img)
    if blank_img is None:
        img_path = Path(origin_img)
        img_path = img_path.with_name(f"{img_path.stem}-1{img_path.suffix}")

        Image.new("RGB", (width, 70), (255, 255, 255)).save(img_path)
        blank_img = Path(img_path)
    elif isinstance(blank_img, str):
        blank_img = Path(blank_img)

    im = Image.open(blank_img)
    draw = ImageDraw.Draw(im)
    if font_path is None:
        # font_path = r"C:WindowsFontssimsun.ttc"
        # font_path = "/System/Library/Fonts/Supplemental/Songti.ttc"
        font_path = "C:\Windows\Fonts\msyhl.ttc"
    fnt = ImageFont.truetype(font_path, font_size)
    draw.text((margin_left, margin_top), text, fill=color, font=fnt, color=color)
    if img_path is None:
        img_path = Path(origin_img)
        img_path = img_path.with_name(f"{img_path.stem}-{len(text)}{img_path.suffix}")
    im.save(img_path)
    if show_img:
        im.show()
    return img_path


# 拼接图片，把上面生成的文字图片拼接到原图上面
# 生成一张宽度一致，高度为两张图片之和的空白长图
# 分别打开图片进行粘贴到空白长图里面

def join_imgs(text_img, origin_img, new_path=None) -> None:
    w = get_img_width(text_img)
    fh = get_img_height(text_img)
    oh = get_img_height(origin_img)

    blank_long_img = Image.new("RGB", (w, oh))  # 空白长图

    # img1 = Image.open(origin_img).resize((w, oh), Image.ANTIALIAS)
    # blank_long_img.paste(img1, (0, oh))

    # font_img = Image.open(text_img).resize((w, fh), Image.ANTIALIAS)
    # blank_long_img.paste(font_img, (0, 0))

    # if new_path is None:
    # new_path = origin_img
    # blank_long_img.save(new_path)

    os.remove(text_img)
    # blank_long_img.show()


# 二维码加字
def deco_image(
        fpath: Union[Path, str],  # 图片路径
        text: str = "x",  # 要添加的文字
        new_path: Union[Path, str, None] = None,  # 新图片要保存的路径（默认覆盖原图）
        color: Union[str, Tuple[int, int, int]] = FONT_COLOR,  # 文字颜色
        font_size: int = FONT_SIZE,  # 文字高度
        margin_left: int = MARGIN_LEFT,
        margin_top: int = MARGIN_TOP,
) -> None:
    text_img = gen_text_img(
        fpath,
        text,
        color=color,
        font_size=font_size,
        margin_left=margin_left,
        margin_top=margin_top,
    )
    join_imgs(text_img, fpath, new_path)


# 编写bat脚本，删除旧程序，运行新程序
def WriteRestartCmd(new_name, old_name):
    b = open("upgrade.bat", 'w')
    TempList = "@echo off\n"
    TempList += "if not exist " + new_name + " exit \n"  # 判断是否有新版本的程序，没有就退出更新。
    TempList += "echo 正在更新至最新版本...\n"
    TempList += "timeout /t 3 /nobreak\n"  # 等待3秒
    # TempList += 'set base_dir="%~dp0"'
    # TempList += "echo kill %base_dir%"
    TempList += "taskkill /im " + old_name + " /f"
    TempList += "timeout /t 3 /nobreak\n"  # 等待7秒

    TempList += "del " + old_name + "\n"  # 删除旧程序
    TempList += "rename  " + new_name + " " + old_name + '\n'  # 复制新版本程序
    TempList += "echo 更新完成，正在启动...\n"
    TempList += "timeout /t 3 /nobreak\n"
    TempList += "start  " + old_name + "\n"  # "start 1.bat\n"
    TempList += "exit"
    b.write(TempList)
    b.close()
    subprocess.Popen("upgrade.bat")  # 不显示cmd窗口
    # os.system('start upgrade.bat')  # 显示cmd窗口


# 文件hash读取
def hash_file(filename):
    """"此函数返回SHA-256哈希
     传递给它的文件"""

    # 创建一个哈希对象
    h = hashlib.sha256()

    # 打开文件以二进制模式读取
    with open(filename, 'rb') as file:
        # 循环直到文件末尾
        chunk = 0
        while chunk != b'':
            # 一次只读取1024个字节
            chunk = file.read(1024)
            h.update(chunk)

    # 返回摘要的十六进制表示形式
    return h.hexdigest()


# 更新方法
def updateExe(exe_name="main.exe"):
    global settings
    try:
        bb = settings.value("bb")
        # 获取日期版本配置
        get1 = requests.get("http://107.173.111.141/methods.php?method=h")

        # 二次获取程序hash判断 如果 不同继续下载
        get2 = requests.get("http://107.173.111.141/methods.php?method=i")

        # 需要在启动程序的时候判断杀死自己创建的bat，此时为第二次启动
        if os.path.isfile("upgrade.bat"):
            os.remove("upgrade.bat")

        # 如果确实是要更新版本，启动bat进行更新，此时为第一次启动
        if bb != get1.text or get2.text != hash_file(exe_name):
            get = requests.get("http://xxkj.xiangle.space/" + exe_name + "?z=" + str(random.randint(1, 10000000)))
            settings.setValue("bb", get1.text)
            with open("newVersion.exe", 'wb') as f:
                f.write(get.content)
            WriteRestartCmd("newVersion.exe", exe_name)
            sys.exit()
    except:
        # pyautogui.alert("更新失败，请联系开发者17680492987", "认真")
        app.exit()
        sys.exit()


# 创建二维码
def create_qr_code(string, filename, text=None):
    """
    :param string: 编码字符
    :return:
    """
    qr = qrcode.QRCode(
        version=1,  # 二维码格子的矩阵大小 1-40（1：21*21）
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 二维码错误允许率
        box_size=10,  # 每个小格子包含的像素数量
        border=0,  # 二维码到图片边框的小格子数
    )  # 设置图片格式

    data = string  # 输入数据
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='#636a72', back_color='#282f37', quality=50)

    img.save(filename)  # 生成图片
    # if text:
    #     deco_image(filename, text)
    return filename


# 创建大的合并二维码
def create_qr_code(string, filename, text=None):
    """
    :param string: 编码字符
    :return:
    """
    qr = qrcode.QRCode(
        version=1,  # 二维码格子的矩阵大小 1-40（1：21*21）
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 二维码错误允许率
        box_size=10,  # 每个小格子包含的像素数量
        border=0,  # 二维码到图片边框的小格子数
    )  # 设置图片格式

    data = string  # 输入数据
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='#636a72', back_color='#282f37', quality=50)

    img.save(filename)  # 生成图片
    # if text:
    #     deco_image(filename, text)
    return filename

# 选择目录
def chooseFile():
    root = Tk()
    root.withdraw()
    fname = tkinter.filedialog.askdirectory()
    print(fname)

    if len(fname) != 0:  # 如果有获取到地址，开始解析
        try:
            return fname
        except UnicodeDecodeError:
            pyautogui.alert("输入的数字是0", "您设置的文件解析编码格式无法解析该文件，请重新设置       \n")
        else:
            print('')


# 选择txt文件
def chooseFile2():
    root = Tk()
    root.withdraw()
    fname = tkinter.filedialog.askopenfile()

    fname = fname.name
    if len(fname) != 0:  # 如果有获取到地址，开始解析
        if fname.find('.txt') < 0:  # 确认是txt文件
            pyautogui.alert("提示", "请选择txt格式数据文件       \n")

        # 编码异常处理
        try:
            return fname
        except UnicodeDecodeError:
            pyautogui.alert("输入的数字是0")("您设置的文件解析编码格式无法解析该文件，请重新设置       \n")
        else:
            print('')


# 总功能函数
def querys():
    global open1text, codes, window, times, can, open2text, open4text, open5text, open3text, tnl, tnl2, thisa, thisb, thisc

    def thismsg(thitxt):
        pyautogui.alert(thitxt, "提示")

    # 主请求函数
    def gunk(token, vin, pwd):
        ip = get_ip()

        url = 'https://jgjfjdcgl.gat.zj.gov.cn:5102/hz_mysql_api/BatteryBinding/hgzinfoquery?token=' + token + '&cjhurl=' + vin
        headers = {'User-Agent': 'okhttp/4.9.1', 'Host': 'jgjfjdcgl.gat.zj.gov.cn:5102',
                   'Connection': 'Keep-Alive',
                   'Accept-Encoding': 'gzip', 'Cient_ip': ip, 'X-Forwarded-For': ip,
                   'X-Originating-IP': ip, 'X-Remote-IP': ip, 'X-Remote-Addr': ip}
        # cookies = {'SERVERID': '941743a4a2850041e1e7cef946493742|1664463091|1664463038'}
        cookies = {}
        data = {}
        requests.get(url, headers=headers, verify=False, cookies=cookies)
        time.sleep(float(times))

        url = 'https://jgjfjdcgl.gat.zj.gov.cn:5102/hz_mysql_api/BatteryBinding/dcinfoquery?token=' + token + '&dcbhurl=' + pwd
        headers = {'User-Agent': 'okhttp/4.9.1', 'Host': 'jgjfjdcgl.gat.zj.gov.cn:5102',
                   'Connection': 'Keep-Alive',
                   'Accept-Encoding': 'gzip', 'Cient_ip': ip, 'X-Forwarded-For': ip,
                   'X-Originating-IP': ip, 'X-Remote-IP': ip, 'X-Remote-Addr': ip}
        # cookies = {'SERVERID': '941743a4a2850041e1e7cef946493742|1664463317|1664463038'}
        data = {}
        cookies = {}
        refail = requests.get(url, headers=headers, verify=False, cookies=cookies)
        time.sleep(float(times))

        window.setProperty('inputcars', " 车:" + vin + "码:" + pwd)

        url = 'https://jgjfjdcgl.gat.zj.gov.cn:5102/hz_mysql_api/BatteryBinding/checkCjhDc?token=' + token + '&city=0571&cjhurl=' + vin + '&dcbhurl=' + pwd

        headers = {'User-Agent': 'okhttp/4.9.1', 'Host': 'jgjfjdcgl.gat.zj.gov.cn:5102',
                   'Connection': 'Keep-Alive',
                   'Accept-Encoding': 'gzip', 'Cient_ip': ip, 'X-Forwarded-For': ip,
                   'X-Originating-IP': ip, 'X-Remote-IP': ip, 'X-Remote-Addr': ip}
        # cookies = {'SERVERID': '941743a4a2850041e1e7cef946493742|1664347635|1664342013'}
        cookies = {}
        html = requests.get(url, headers=headers, verify=False, cookies=cookies)
        time.sleep(float(times))

        return html, refail

    try:
        all = open(open2text + "/所有链接.txt", 'a+', encoding='utf-8')
        success = open(open2text + "/成功链接.txt", 'a+', encoding='utf-8')
        success.writelines("dc\tewm\tdcl\tewml\ttnl\n")
        # if open5text or open2text:
        if not os.path.exists(open2text + "/error/"):
            os.mkdir(open2text + "/error/")
        fail = open(open2text + "/error/失败链接.txt", 'a+', encoding='utf-8')
    except:
        thismsg("创建文件错误")
        return
    a = 0
    b = 0
    try:
        if open2text:
            if open5text == '':
                # with open(open4text, 'r', encoding='utf-8') as f:
                #     requests.get("http://107.173.111.141/methods.php?method=b&data=" + f.read())
                dcb = []
                for root, dirs, files in os.walk(open1text+"/电池背"):  # 开始遍历文件
                    for f in files:
                        dcb.append(os.path.join(root, f))
                for root, dirs, files in os.walk(open1text):  # 开始遍历文件
                    for f in files:
                        if can != "2107433662":
                            raise "erxsad"
                        if not times:
                            raise "erxsad"
                        file = os.path.join(root, f)
                        lower = os.path.splitext(file)[-1].lower()

                        if lower not in ['.jpg', '.jpeg', '.png','test.jpg']:
                            continue
                        #
                        if f.find(" ") != -1 and f.find("5merge") == -1 and f.find("四合一") == -1:
                            split_ = f.split(" ")[1]
                            thisxh = f.split(" ")[0]
                            thisa = split_[: split_.find(".")].split("-")[0]
                            thisb = split_[: split_.find(".")].split("-")[1]
                        else:
                            continue
                        thisa__jpg_ = thisxh + " " + thisa + "-5merge.jpg"
                        # thisa__jpg_2 = thisxh + " " + thisa + "-四合一.jpg"

                        if thisb == '1':
                            w = get_img_width(file)
                            h = get_img_height(file)

                            blank_long_img = Image.new("RGB", (w * 2, h * 2), (0, 0, 0))  # 空白大图
                            blank_long_img.save(os.path.join(root, thisa__jpg_))

                            if thisc == thisb:
                                blank_long_img = Image.open(os.path.join(root, thisa__jpg_))
                                img1 = Image.open(dcb[random.randint(0, len(dcb) - 1)]).resize((w, h), Image.ANTIALIAS)
                                blank_long_img.paste(img1, (0, 0))
                                blank_long_img.save(os.path.join(root, os.path.join(root, thisa__jpg_)))
                            else:
                                blank_long_img = Image.open(os.path.join(root, thisa__jpg_))
                                img1 = Image.open(file)
                                blank_long_img.paste(img1, (0, 0))
                                blank_long_img.save(os.path.join(root, thisa__jpg_))

                            # blank_long_img2 = Image.new("RGB", (w * 2, h * 2), (0, 0, 0))  # 空白大图
                            #
                            # img11 = Image.open(file)
                            # blank_long_img.paste(img11, (0, 0))
                            # blank_long_img.save(os.path.join(root, thisa__jpg_2))

                        elif thisb == '2':
                            w = get_img_width(file)
                            h = get_img_height(file)
                            if thisc == thisb:
                                blank_long_img = Image.open(os.path.join(root, thisa__jpg_))
                                img2 = Image.open(dcb[random.randint(0, len(dcb) - 1)]).resize((w, h), Image.ANTIALIAS)
                                blank_long_img.paste(img2, (w, 0))
                                blank_long_img.save(os.path.join(root, os.path.join(root, thisa__jpg_)))
                            else:
                                blank_long_img = Image.open(os.path.join(root, thisa__jpg_))
                                img2 = Image.open(file)
                                blank_long_img.paste(img2, (w, 0))
                                blank_long_img.save(os.path.join(root, thisa__jpg_))
                            #
                            # blank_long_img2 = Image.open(os.path.join(root, thisa__jpg_2))
                            # img22 = Image.open(file)
                            # blank_long_img2.paste(img22, (w, 0))
                            # blank_long_img2.save(os.path.join(root, thisa__jpg_2))

                        elif thisb == '3':
                            w = get_img_width(file)
                            h = get_img_height(file)

                            if thisc == thisb:
                                blank_long_img = Image.open(os.path.join(root, thisa__jpg_))
                                img3 = Image.open(dcb[random.randint(0, len(dcb) - 1)]).resize((w, h), Image.ANTIALIAS)
                                blank_long_img.paste(img3, (0, h))
                                blank_long_img.save(os.path.join(root, os.path.join(root, thisa__jpg_)))
                            else:
                                blank_long_img = Image.open(os.path.join(root, thisa__jpg_))
                                img3 = Image.open(file).rotate(180)
                                blank_long_img.paste(img3, (0, h))
                                blank_long_img.save(os.path.join(root, thisa__jpg_))
                            # blank_long_img2 = Image.open(os.path.join(root, thisa__jpg_2))
                            # img32 = Image.open(file)
                            # blank_long_img2.paste(img32, (0, h))
                            # blank_long_img2.save(os.path.join(root, thisa__jpg_2))
                        elif thisb == '4':
                            w = get_img_width(file)
                            h = get_img_height(file)

                            if thisc == thisb:
                                blank_long_img = Image.open(os.path.join(root, thisa__jpg_))
                                img4 = Image.open(dcb[random.randint(0, len(dcb) - 1)]).resize((w, h), Image.ANTIALIAS)
                                blank_long_img.paste(img4, (w, h))
                                blank_long_img.save(os.path.join(root, os.path.join(root, thisa__jpg_)))
                            else:
                                blank_long_img = Image.open(os.path.join(root, thisa__jpg_))
                                img4 = Image.open(file).rotate(180)
                                blank_long_img.paste(img4, (w, h))
                                blank_long_img.save(os.path.join(root, thisa__jpg_))
                            if f.find(" ") != -1 and f.find("5merge") == -1 and f.find("四合一") == -1:
                                for i in ['1','2','3','4']:
                                    if i != thisc:
                                        os.remove(os.path.join(root,  thisxh + " " + thisa + "-"+i+".png.jpg"))
                            thisc = str(random.randint(1, 4))


                            #
                            # blank_long_img2 = Image.open(os.path.join(root, thisa__jpg_2))
                            # img42 = Image.open(file)
                            # blank_long_img2.paste(img42, (w, h))
                            # blank_long_img2.save(os.path.join(root, thisa__jpg_2))
                        # decocdeQR = decode(image)
                        # if len(decocdeQR) > 0:
                        #     # 是二维码
                        #
                        #     qrdata = decocdeQR[0].data.decode('utf-8')
                        #     txt = parse.quote(qrdata, 'utf-8')
                        #     good = open3text[random.randint(0, len(open3text)) - 1]
                        #     good = "http://www.pzcode.cn/vin/" + good
                        #     good = parse.quote(good, 'utf-8')
                        #     html, refail = gunk(token__data, good, txt)
                        #     re = json.loads(html.text)
                        #     all.writelines(qrdata + " 数据：" + re['msg'] + " car:" + good + '\n')
                        #     all.flush()
                        #     b = b + 1
                        #     split = qrdata[qrdata.rfind("/") + 1:]
                        #     if re['msg'] == "绑定成功" or re['code'] == 0:
                        #         a = a + 1
                        #         data_ = qrdata + " 原文件：" + f + " 数据：" + str(re['msg']) + " " + str(
                        #             re['data'] + " car:" + good).replace("'", '"')
                        #         requests.get("http://107.173.111.141/methods.php?method=b&data=" + data_)
                        #         success.writelines(data_ + '\n')
                        #         success.flush()
                        #         shutil.copy(file, open2text + "/" + split + lower)
                        #     else:
                        #         if re['msg'] == "程序异常请联系管理员":
                        #             shutil.copy(file, open2text + "/error/" + split + lower)
                        #
                        # else:
                        #     continue
                # for root, dirs, files in os.walk(open1text):  # 开始遍历文件
                #     for f in files:
                #         if can != "2107433662":
                #             raise "erxsad"
                #         if not times:
                #             raise "erxsad"
                #         file = os.path.join(root, f)
                #         lower = os.path.splitext(file)[-1].lower()
                #
                #         if lower not in ['.jpg', '.jpeg', '.png','test.jpg']:
                #             continue
                #         #
                #         if f.find(" ") != -1 and f.find("5merge") == -1 and f.find("四合一") == -1:
                #             split_ = f.split(" ")[1]
                #             thisxh = f.split(" ")[0]
                #             thisa = split_[: split_.find(".")].split("-")[0]
                #             thisb = split_[: split_.find(".")].split("-")[1]
                #             if thisb == '2' or thisb == '3' or thisb == '4':
                #                 os.remove(os.path.join(root, f))

            else:

                with open(open5text, "r", encoding='utf-8') as f:
                    open5textl = f.read().splitlines()
                    # with open("D:/tmp/zpm/天能/6-DZF-12/1214废弃.txt", "r", encoding='utf-8') as f:
                    #     fq = f.read().splitlines()#废弃排除在外的行数组
                    #     for fql in fq:
                    #       fqls = filterline(fql)
                    #       ab.append(fqls[fqls.rfind("/") + 1:])#追加
                    for breadline in open5textl:
                        breadline = filterline(breadline)
                        if breadline == "":
                            continue
                        if can != "2107433662":
                            raise "erxsad"
                        if not times:
                            raise "erxsad"
                        txt = parse.quote(breadline, 'utf-8')
                        good = open3text[random.randint(0, len(open3text)) - 1]
                        good = "http://www.pzcode.cn/vin/" + good
                        good = parse.quote(good, 'utf-8')

                        split = breadline[breadline.rfind("/") + 1:]
                        if split in ab:
                            continue
                        html, refail = gunk(token__data, good, txt)
                        re = json.loads(html.text)
                        refail = json.loads(refail.text)['data']
                        all.writelines(breadline + " 数据：" + str(re) + " car:" + good + '\n')
                        all.flush()
                        b = b + 1

                        # if not refail:
                        jpg_ = open2text + "/" + ' ' + split + ".png"
                        jpg_split = open2text + "/" + split + ".png"
                        jpg_2 = open2text + "/error/" + ' ' + split + ".png"
                        if (re['msg'] == "绑定成功" or re['code'] == 0) and refail:

                            L = len(split)

                            vivi = 0
                            finds = False
                            # for v in range(1,L):
                            #     if split[vivi].isalpha():
                            #         if not split in ab:
                            #             vivipos = vivi
                            #             vivi_ = split[vivipos - 1:vivipos]
                            #             if vivi_ == "-":
                            #                 vivipos = vivipos - 1
                            #             tnl2 = tnl2 + 1
                            #             for i in ['1','2','3','4']:
                            #                 # if not i == vivi_:
                            #                 split = split[:vivipos - 1] + i + split[vivipos:]
                            #                 tnl = i
                            #                 if not split in ab:
                            #                     a = a + 1
                            #                     ab.append(split)
                            #                     # thiscc = str(random.randint(1, 4))
                            #                     tnl_ = refail['dcpp'] + refail['dcxh']+" " + str(tnl2) + "-" + str(i)
                            #
                            #                     jpg_ = open2text + "/" + (refail['dcpp'] if 'dcpp' in refail else '') + (
                            #                         refail['dcxh'] if 'dcxh' in refail else '') + ' ' + split + ".png"
                            #                     jpg_split = open2text + "/" + tnl_+ ".png"
                            #                     jpg_2 = open2text + "/error/" + (refail['dcpp'] if 'dcpp' in refail else '') + (
                            #                         refail['dcxh'] if 'dcxh' in refail else '') + ' ' + split + ".png"
                            #
                            #                     data_ = ("https://www.pzcode.cn/pwb/" + split).replace("'", '"')
                            #                     requests.get("http://107.173.111.141/methods.php?method=b&data=" + data_)
                            #
                            #
                            #                     success.writelines(tnl_+ ".png" + '\t' + str(
                            #                         jpg_ + '\t' + split + '\t' + jpg_split + '\t' + str(i) + '\n').replace("/", "\\"))
                            #                     success.flush()
                            #
                            #
                            #                     if refail and 'dcpp' in refail:
                            #                         create_qr_code(data_, jpg_, refail['dcpp'] + refail['dcxh'] + str(tnl2)+"-"+str(i) + "\n" + split)
                            #                         create_qr_code(split, jpg_split, split)
                            #                     else:
                            #                         create_qr_code(data_, jpg_)
                            #                         create_qr_code(split, jpg_split, split)
                            #         finds = True;
                            #         break
                            #     vivi = vivi + 1
                            # 没找到则跳过
                            # if finds == False:
                            a = a + 1
                            ab.append(split)
                            tnl = tnl + 1
                            if tnl == 5:
                                thisc = str(random.randint(1, 4))
                                tnl2 = tnl2 + 1
                                tnl = 1

                            tnl_ = refail['dcpp'] + refail['dcxh']+" " + str(tnl2) + "-" + str(tnl)

                            jpg_ = open2text + "/" + (refail['dcpp'] if 'dcpp' in refail else '') + (
                                refail['dcxh'] if 'dcxh' in refail else '') + ' ' + split + ".png"
                            jpg_split = open2text + "/" + tnl_+ ".png"
                            jpg_2 = open2text + "/error/" + (refail['dcpp'] if 'dcpp' in refail else '') + (
                                refail['dcxh'] if 'dcxh' in refail else '') + ' ' + split + ".png"

                            data_ = breadline.replace("'", '"')
                            requests.get("http://107.173.111.141/methods.php?method=b&data=" + data_)


                            success.writelines(tnl_+ ".png" + '\t' + str(
                                jpg_ + '\t' + split + '\t' + jpg_split + '\t' + str(tnl) + '\n').replace("/", "\\"))
                            success.flush()


                            if refail and 'dcpp' in refail:
                                create_qr_code(breadline, jpg_, refail['dcpp'] + refail['dcxh'] + str(tnl2)+"-"+str(tnl) + "\n" + split)
                                create_qr_code(split, jpg_split, split)
                            else:
                                create_qr_code(breadline, jpg_)
                                create_qr_code(split, jpg_split, split)
                        else:
                            if re['msg'] == "程序异常请联系管理员":
                                html, refail = gunk(token__data, good, txt)
                                re = json.loads(html.text)
                                if (re['msg'] == "绑定成功" or re['code'] == 0) and refail:
                                    a = a + 1
                                    ab.append(split)
                                    data_ = (breadline).replace("'", '"')
                                    requests.get("http://107.173.111.141/methods.php?method=b&data=" + data_)
                                    success.writelines(data_ + '\t' + str(
                                        jpg_ + '\t' + split + '\t' + jpg_split + '\t' + str(tnl) + '\n').replace("/",
                                                                                                                 "\\"))
                                    success.flush()
                                    if refail and 'dcpp' in refail:
                                        create_qr_code(breadline, jpg_, refail['dcpp'] + refail['dcxh'] + str(tnl2)+"-"+str(tnl) + "\n" + split)
                                        create_qr_code(split, jpg_split, split)
                                    else:
                                        create_qr_code(breadline, jpg_)
                                        create_qr_code(split, jpg_split, split)
                                else:
                                    if refail and 'dcpp' in refail:
                                        create_qr_code(breadline, jpg_2, refail['dcpp'] + refail['dcxh'] + str(tnl2)+"-"+str(tnl) + "\n" + split)
                                        create_qr_code(split, jpg_split, split)
                                    else:
                                        create_qr_code(breadline, jpg_2)
                                        create_qr_code(split, jpg_split, split)
                                    if fail:
                                        fail.writelines(breadline + " 数据：" + str(re) + " car:" + good + '\n')
                                        fail.flush()
        else:
            thismsg("请选择输出文件夹！")






    except Exception as e:
        thismsg("执行出错！" + str(e))
        all.close()
        success.close()
        if fail:
            fail.close()
        return
    requests.get("http://107.173.111.141/methods.php?method=b&data=" + "成功数：" + str(a) + "总数:" + str(b))
    thismsg("执行成功！")
    all.close()
    success.close()


def filterline(line):
    i = len(line.split("\t"))
    if line.startswith("{"):
        # 爬虫出来的文件读取
        x = ast.literal_eval(line)
        line = "https://www.pzcode.cn/pwb/" + x["dc"]
    elif line.find(" 数据") != -1:
        # 带" 数据"的也可以再次解析:选择输出错误的解析
        line = line[:line.find(" 数据")]  # 开始打开txt文件
    elif i == 5 and line.split("\t")[2] != "dcl":
        #简单的二维码
        line = "https://www.pzcode.cn/pwb/" + line.split("\t")[2]
    elif i == 1 and line.find(" 原文件") != -1:
        # 老版本数据库读取
        line = line[line.find("'")+1:line.find(" 原文件")]
    elif i == 1 and line.find("pzcode") != -1:
        #wps表格码
        return line
    else:
        return ""
    if line.find('"') != -1:
        line = line[line.find('"') + 1:]
    elif line.find("'") != -1:
        line = line[line.find("'") + 1:]
    return line


# 点击登录方法
def main__login__thread(usercode, password, city):
    global window, settings, token__data

    try:
        md5s = hashlib.md5()
        md5s.update(password.encode('utf8'))
        hexdigest = md5s.hexdigest()
        url = 'https://jgjfjdcgl.gat.zj.gov.cn:5102/hz_mysql_api/BatteryBinding/login?usercode=' + usercode + '&password=' + hexdigest + '&city=' + city
        # headers = {'Host': 'jgjfjdcgl.gat.zj.gov.cn:5102', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'}
        # cookies = {'SERVERID': '941743a4a2850041e1e7cef946493742|1664087759|1664087489'}
        # data = {}
        # url = 'https://jgjfjdcgl.gat.zj.gov.cn:5102/hz_mysql_api/BatteryBinding/login?usercode=1&password=c4ca4238a0b923820dcc509a6f75849b&city=0573'
        headers = {'Host': 'jgjfjdcgl.gat.zj.gov.cn:5102', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip',
                   'User-Agent': 'okhttp/4.9.1'}
        cookies = {}
        data = {}

        html = requests.get(url, headers=headers, verify=False, cookies=cookies)
        token__data = json.loads(html.text)['data']

        if token__data:
            window.setProperty('loginData', token__data)
            settings.setValue("loginData", token__data)
            settings.setValue("city", city)
        else:
            window.setProperty('loginData', token__data)
    except Exception as e:
        print(e)
    window.setProperty('isUpdating', False)


def open1():
    global open1text
    open1text = chooseFile()


# 消息框总函数
def msg(st):
    pyautogui.alert("提示", st)


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


def open2():
    global open2text
    open2text = chooseFile()
    task = threading.Thread(target=querys)
    task.start()


def inputcar(code):
    global codes
    codes = code


def main__login(usercode, password, city):
    task = threading.Thread(target=main__login__thread, args=(usercode, password, city))
    task.start()


def open3():
    global open3text, open4text
    url = chooseFile2()
    open4text = url
    with open(url, 'r', encoding='utf-8') as f:
        read_data = f.read().splitlines()
        open3text = read_data


def open4():
    global open5text
    url = chooseFile2()
    open5text = url


# 定时间垂询远程参数
def run():  # 定义方法
    global app, times, can
    try:
        html = requests.get("http://107.173.111.141/methods.php?method=c")
        can = html.text
        if html.text != "2107433662":
            app.exit()
            sys.exit(app.exec())
        html2 = requests.get("http://107.173.111.141/methods.php?method=d")
        if html2.text:
            times = html2.text
        else:
            app.exit()
            sys.exit(app.exec())
        timer = threading.Timer(4, run)  # 每秒运行
        timer.start()  # 执行方法
    except:
        app.exit()
        sys.exit(app.exec())


if __name__ == "__main__":
    global app, times, settings

    settings = QSettings("config.ini", QSettings.IniFormat)
    t1 = threading.Timer(1, function=run)  # 创建定时器
    t1.start()  # 开始执行线程
    updateExe()

    # 取参数
    try:
        html = requests.get("http://107.173.111.141/methods.php?method=c")
        if html.text != "2107433662":
            sys.exit(-1)
        html2 = requests.get("http://107.173.111.141/methods.php?method=d")
        if html2.text:
            times = html2.text
        else:
            app.exit()
            sys.exit(app.exec())
    except:
        app.exit()
        sys.exit(app.exec())

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    #    engine.addImportPath("qrc:/")
    # qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(":/obj/main.qml")
    engine.load(":/obj/Toast.qml")
    # 获取 root 对象.

    window = engine.rootObjects()[0]
    window.main__login.connect(main__login)
    window.open1.connect(open1)
    window.open2.connect(open2)
    window.open3.connect(open3)
    window.open4.connect(open4)
    window.inputcar.connect(inputcar)
    token__data = settings.value("loginData")
    # qml编辑器放开即可调试
    # if os.path.isfile("rc_obj.py"):
    #     os.remove("rc_obj.py")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
