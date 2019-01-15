#!/usr/bin/env python
#encoding:utf-8
'''
author: yangmingwei
'''
from . import main
from .. import scheduler
from flask import request
import json
from app.public import DateEncoder
from app.job.core import jobfromparm,get_job_logs

@main.route('/pause',methods=['POST'])
def pause_job():
    '''暂停作业'''
    response = {'status': '-1'}
    try:
        data = request.get_json(force=True)
        job_id = data.get('id')
        scheduler.pause_job(job_id)
        response['msg'] = "job[%s] pause success!"%job_id
        response['status'] = 0
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response)

@main.route('/resume',methods=['POST'])
def resume_job():
    '''恢复作业'''
    response = {'status': '-1'}
    try:
        data = request.get_json(force=True)
        job_id = data.get('id')
        scheduler.resume_job(job_id)
        response['msg'] = "job[%s] resume success!"%job_id
        response['status'] = 0
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response)

@main.route('/remove',methods=['DELETE'])
def reomve_jobs():
    '''删除作业'''
    response = {'status': '-1'}
    try:
        data = request.get_json(force=True)
        job_id = data.get('id')
        if job_id != 'all':
            scheduler.remove_job(job_id)
            response['msg'] = "job[%s] remove success!"%job_id
        else:
            scheduler.remove_all_jobs()
            response['msg'] = "job all remove success!"
        response['status'] = 0
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response)

@main.route('/edit', methods=['POST'])
def edit_job():
    '''修改作业'''
    response = {'status': '-1'}
    try:
        data = request.get_json(force=True)
        job_id = data.get('id')
        old_job = scheduler.get_job(job_id)
        if old_job:
            jobfromparm(scheduler,**data)
            response['status'] = 0
            response['message'] = "job[%s] edit success!"%job_id
        else:
            response['message'] = "job[%s] Not Found!"%job_id
    except Exception as e:
        response['message'] = str(e)
    return json.dumps(response)

@main.route('/add', methods=['POST'])
def add_job():
    '''新增作业'''
    response = {'status': '-1'}
    try:
        data = request.get_json(force=True)
        job_id = jobfromparm(scheduler,**data)
        response['status'] = 0
        response['msg'] = "job[%s] add success!"%job_id
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response)

@main.route('/', methods=['GET'])
def show_jobs():
    '''获取所有jobs信息'''
    response = {}
    try:
        jid = request.args.get('id')
        if jid == None:
            ret_list = scheduler.get_jobs()
        else:
            ret_list = [scheduler.get_job(jid)]
        inof_list = []
        for ret in ret_list:
            fields = ret.trigger.fields
            cron = {}
            for field in fields:
                cron[field.name] = str(field)
            cron_list = [cron['second'],cron['minute'],cron['hour'],cron['day'],cron['month'],cron['day_of_week']]
            info = {
                'id':ret.id,
                'next_run_time':ret.next_run_time,
                'cmd':ret.kwargs.get('cmd'),
                #'func':ret.func_ref,
                'status':'running' if ret.next_run_time != None else 'stop',
                'cron':' '.join(cron_list)
            }
            inof_list.append(info)
        response['status'] = 0
        response['data'] = inof_list
        response['count'] = len(inof_list)
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response,cls=DateEncoder)

@main.route('/log', methods=['GET'])
def job_log():
    '''获取所有job log信息'''
    response = {}
    try:
        ret = get_job_logs(request.args)
        response['status'] = 0
        response['data'] = ret
        response['count'] = len(ret)
    except Exception as e:
        response['msg'] = str(e)
    return json.dumps(response,cls=DateEncoder)
