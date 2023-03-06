# coding=utf-8
import os
import json
import subprocess
from datetime import datetime
import importlib
# 使用 import_module 导入模块并确保只导入一次
timetask = importlib.import_module('timetask')

class JsonRead:
    def __init__(self, d):
        self.__dict__ = d

if __name__ =="__main__":
    with open('./blackgo.json', 'r', encoding='utf-8') as f:
        jsonStr = f.read()
        config = json.loads(jsonStr, object_hook=JsonRead)
        if "gitParameter" in dir(config):
            if config.gitParameter.timedelta:
                timetask.git_monitor(config.gitParameter.timedelta)
            else:
                print("未设置git 拉取时间 timedelta") / exit()
            if "panicBuying" in dir(config):
                buy = config.panicBuying
                if len(list(buy)) == 0:
                    print("抢购包数据条数为0") / exit()
                for item in buy:
                    name = item.name if "name" in dir(item) else print("name不存在") / exit()
                    if item.enable:
                        print("执行" + name + "软件包")
                        runscript = "python " + name + "/" + name + ".py --time \"" + item.time + "\" --type " + str(
                            item.type) + " --desc " + item.desc if "desc" in dir(item) else ""
                        subprocess.Popen(runscript)
                    else:
                        print(item.name, "已经关闭")
                    # os.system("pause")
        else:
            print("没有git配置，程序退出")
        f.close()

    print("now time", datetime.now())
