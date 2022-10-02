# coding=utf-8
import os
import random
import subprocess
import sys
import hashlib

import pyautogui
import requests
#用于4秒计时器销魂前的反调试更新小包，让调试者无法调试

# 全局参数
global open1text, open2text, app, codes, open3txt, times, settings, open4teext, open5text

# 编写bat脚本，删除旧程序，运行新程序
def WriteRestartCmd(new_name, old_name):
    b = open("upgrade.bat", 'w')
    TempList = "@echo off\n"
    TempList += "if not exist " + new_name + " exit \n"  # 判断是否有新版本的程序，没有就退出更新。
    TempList += "echo 正在更新至最新版本...\n"
    TempList += "timeout /t 10 /nobreak\n"  # 等待10秒
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
    """"此函数返回SHA-1哈希
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
    pyautogui.alert(hash_file(exe_name), "提示")

    try:
        bb = settings.value("bb")
        #获取日期版本配置
        get1 = requests.get("http://193.218.201.80/method.php?method=h")

        # 二次获取程序hash判断 如果 不同继续下载
        get2 = requests.get("http://193.218.201.80/method.php?method=i")

        # 需要在启动程序的时候判断杀死自己创建的bat，此时为第二次启动
        if os.path.isfile("upgrade.bat"):
            os.remove("upgrade.bat")

        # 如果确实是要更新版本，启动bat进行更新，此时为第一次启动
        if bb != get1.text or get2.text != hash_file(exe_name):
            get = requests.get("http://xxkj.xiangle.space/" + exe_name + "?z=" + str(random.randint(1, 10000000)))
            with open("newVersion.exe", 'wb') as f:
                f.write(get.content)
            WriteRestartCmd("newVersion.exe", exe_name)
            sys.exit()
    except:
        # pyautogui.alert("更新失败，请联系开发者17680492987", "认真")
        app.exit()
        sys.exit()


if __name__ == "__main__":

    updateExe()
    pyautogui.alert(hash_file("main.exe"), "提示")
