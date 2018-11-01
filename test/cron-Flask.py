#!/usr/bin/env python
#encoding:utf-8
from flask import Flask
from flask_apscheduler import APScheduler
from flask import request
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import pickle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import subprocess
import json
import datetime
from datetime import date

def exec_shell(cmd):
    '''执行shell命令函数'''
    sub2 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = sub2.communicate()
    ret = sub2.returncode
    if ret == 0:
        return ret, stdout.decode('utf-8').split('\n')
    else:
        return ret, stdout.decode('utf-8').replace('\n', '')

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

app = Flask(__name__)
scheduler = APScheduler()

class Config(object):
    JOBS = [ ]
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='mysql+pymysql://root:chaBUljXrcyn74F@172.16.0.121:3306/stask?charset=utf8')
    }
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }
    SCHEDULER_API_ENABLED = True

def exe_cmd(cmd):
    '''执行CMD命令'''
    recode, stdout = exec_shell(cmd)
    if recode != 0:
        print('[Error] (%s) failed'%cmd)
        exit(407)
    else:
        print('[Success] (%s) success'%cmd)
    return stdout

def jobfromparm(**jobargs):
    id = jobargs['id']
    #func=__name__+':'+jobargs['func']
    func=__name__+':'+'exe_cmd'
    #args = eval(jobargs['args'])   #多个参数
    args = jobargs['cmd']
    trigger = jobargs['trigger']
    seconds = jobargs.get('seconds')
    hour = jobargs.get('hour')
    minute = jobargs.get('minute')
    print('[add job]: ',id)
    if trigger == 'interval':
        scheduler.add_job(func=func,id=id, kwargs={'cmd':args},trigger=trigger,seconds=seconds,replace_existing=True)
    elif trigger == 'cron':
        scheduler.add_job(func=func,id=id, kwargs={'cmd':args},trigger=trigger,hour=hour,minute=minute,replace_existing=True)
    return id

@app.route('/pause',methods=['GET', 'POST'])
def pause_job():
    '''暂停作业'''
    data = request.get_json(force=True)
    job_id = data.get('id')
    scheduler.pause_job(job_id)
    return "job[%s] pause success!"%job_id

@app.route('/resume',methods=['GET', 'POST'])
def resume_job():
    '''恢复作业'''
    data = request.get_json(force=True)
    job_id = data.get('id')
    scheduler.resume_job(job_id)
    return "job[%s] resume success!"%job_id

@app.route('/delete',methods=['GET', 'POST'])
def delete_job():
    '''删除作业'''
    data = request.get_json(force=True)
    job_id = data.get('id')
    scheduler.remove_job(job_id)
    return "job[%s] delete success!"%job_id

@app.route('/delete_all',methods=['GET', 'POST'])
def delete_jobs():
    '''删除作业'''
    print('delete...')
    scheduler.remove_all_jobs()
    return "job all delete success!"


# @app.route('/delete',methods=['GET', 'POST'])
# def modify_job():
#     '''修改作业,未测试'''
#     data = request.get_json(force=True)
#     job_id = data.get('id')
#     scheduler.modify_job(job_id)
#     return "job[%s] resume success!"%job_i


@app.route('/add', methods=['GET', 'POST'])
def add_job():
    '''新增作业'''
    data = request.get_json(force=True)
    print('data-->',data)
    job = jobfromparm(**data)
    return "job[%s] add success!"%job




@app.route('/job',methods=['GET', 'POST'])
def show_job():
    '''获取指定job信息'''
    jid = request.args.get('id')
    ret = scheduler.get_job(jid)
    info = {
        'id':ret.id,
        'next_run_time':ret.next_run_time,
        'kwargs':ret.kwargs,
        #'interval':ret.trigger.interval,               #datetime.timedelta格式
        'interval_length':ret.trigger.interval_length,  #seconds
        'start_date':ret.trigger.start_date,
        'end_date':ret.trigger.end_date,
    }
    return json.dumps(info,cls=DateEncoder)


@app.route('/jobs', methods=['GET'])
def show_jobs():
    '''获取所有jobs信息'''
    ret_list = scheduler.get_jobs()
    inof_list = []
    for ret in ret_list:
        info = {
            'id':ret.id,
            'next_run_time':ret.next_run_time,
            'kwargs':ret.kwargs,
            #'interval':ret.trigger.interval,               #datetime.timedelta格式
            #'interval_length':ret.trigger.interval_length,  #seconds
            'start_date':ret.trigger.start_date,
            'end_date':ret.trigger.end_date,
        }
        inof_list.append(info)
    return json.dumps(inof_list,cls=DateEncoder)

# @app.route('/job', methods=['GET'])
# def show_job():
#     '''获取指定job信息'''
#     jid = request.args.get('id')
#     ret = get_job(jid)
#     print(ret)
#     return ret


# @app.route('/jobs', methods=['GET'])
# def show_jobs():
#     '''获取所有jobs信息'''
#     ret = get_jobs()
#     print(ret)
#     return ret



if __name__ == '__main__':
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run()



'''
新增
curl -i -X POST -H "'Content-type':'appon/x-www-form-urlencoded', 'charset':'utf-8', 'Accept': 'text/plain'" -d '{"id":"test02","cmd":"ifconfig","trigger":"interval","seconds":10}' http://127.0.0.1:5000/add


暂停
curl -i -X POST -H "'Content-type':'appon/x-www-form-urlencoded', 'charset':'utf-8', 'Accept': 'text/plain'" -d '{"id":"test01"}' http://127.0.0.1:5000/pause


恢复
curl -i -X POST -H "'Content-type':'appon/x-www-form-urlencoded', 'charset':'utf-8', 'Accept': 'text/plain'" -d '{"id":"test01"}' http://127.0.0.1:5000/resume

删除
curl -i -X POST -H "'Content-type':'appon/x-www-form-urlencoded', 'charset':'utf-8', 'Accept': 'text/plain'" -d '{"id":"test01"}' http://127.0.0.1:5000/delete

curl -i -X POST -H "'Content-type':'appon/x-www-form-urlencoded', 'charset':'utf-8', 'Accept': 'text/plain'" http://127.0.0.1:5000/delete_all
'''


'''
def exe_sql(sql):
    engine = create_engine("mysql+pymysql://root:chaBUljXrcyn74F@172.16.0.121:3306/bbb_ops?charset=utf8", max_overflow=5)
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    data = session.execute(sql)
    ret = []
    for line in data:
        job_state = line[2]
        result = pickle.loads(job_state)
        trigger = str(result.pop('trigger'))    #trigger类型为IntervalTrigger
        result['trigger'] = trigger
        info = {
            'id':line[0],
            'next_run_time':line[1],
            'job_state':result
        }
        ret.append(info)
    return json.dumps(ret,cls=DateEncoder)

def get_jobs():
    sql = 'select * from apscheduler_jobs'
    ret = exe_sql(sql)
    return ret

def get_job(jid):
    sql = 'select * from apscheduler_jobs WHERE id="%s"'%jid
    ret = exe_sql(sql)
    return ret

'''