from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
import os


class my_CronTrigger(CronTrigger):
    @classmethod
    def from_crontab(cls, expr, timezone=None):
        values = expr.split()
        if len(values) != 6:
            raise ValueError('Wrong number of fields; got {}, expected 6'.format(len(values)))

        return cls(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                   day_of_week=values[5], timezone=timezone)


@atexit.register
def action_shutdown():
    action.shutdown()


def git_task():
    print("git拉取命令执行")
    os.popen("git pull")


def git_monitor(cron):
    action.add_job(git_task, my_CronTrigger.from_crontab(cron), id='git_job', timezone='Asia/Shanghai',
                   replace_existing=True)


def buy_monitor(cron, fun, ids, arg):
    action.add_job(fun, my_CronTrigger.from_crontab(cron), id=ids, kwargs=arg, timezone='Asia/Shanghai',
                   replace_existing=True, max_instances=100)


action = BackgroundScheduler(timezone='Asia/Shanghai', daemon=True)
action.start()
