#!/usr/bin/env python
#encoding:utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import datetime

jobstores = {
    'redis': RedisJobStore(host='172.16.0.121',port=6379,db=0),      #用redis作backend
}

# ZRANGE apscheduler.run_times 0 1
# HGETALL apscheduler.jobs

executors = {
    'default': ThreadPoolExecutor(10),      #默认线程数
    'processpool': ProcessPoolExecutor(3)   #默认进程
}
sched = BlockingScheduler(jobstores=jobstores, executors=executors)

def aps_test():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'H')

# @scheduler.scheduled_job('interval', seconds=3,id='job003')
# def test03():
#     print('test03......')

#添加任务
sched.add_job(func=aps_test, trigger='cron', second='*/5',id='job001',jobstore='redis',replace_existing=True)

#查看任务状态
print(sched.get_job(job_id='job001'))

#移除任务
# scheduler.remove_job('job001')
# print(scheduler.get_job(job_id='job001'))

sched.start()
