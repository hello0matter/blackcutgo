# coding=utf-8
import os
import os.path as osp
import json
import datetime as datetime
from git.repo import Repo
from datetime import datetime, date, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

def Task():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print("time run by ",ts)

def APschedulerMonitor():
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(Task, 'interval', seconds=0.1, id='test_job1')
    # 添加任务,时间间隔5S
    scheduler.add_job(Task, 'interval', seconds=0.1, id='test_job2')
    scheduler.start()

class JsonRead:
    def __init__(self, d):
        self.__dict__ = d

download_path = os.path.join('store')
print("now time",datetime.now())

with open('./blackgo.json', 'r', encoding='utf-8') as f:
    jsonStr = f.read()
    json = json.loads(jsonStr, object_hook=JsonRead)
    if json.gitParameter:
        print(datetime.strptime(json.gitParameter.time, "%Y-%m-%d %H:%M:%S"))
        # new_repo = Repo.clone_from(url='git@github.com:gcsdfaksh/blackcutgo.git', to_path=download_path)
        # repo = Repo.clone_from('https://github.com/gcsdfaksh/blackcutgo.git',
        #                            osp.join(download_path), branch='master')
        if ~os.path.exists(download_path):
            os.mkdir(download_path)
        os.chdir(download_path)
    else:
        print("没有git配置，程序退出")

