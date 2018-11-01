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
    response = {}
    try:
        data = request.get_json(force=True)
        job_id = data.get('id')
        scheduler.pause_job(job_id)
        response['message'] = "job[%s] pause success!"%job_id
        response['status'] = True
    except Exception as e:
        response['message'] = str(e)
    return json.dumps(response)

@main.route('/resume',methods=['POST'])
def resume_job():
    '''恢复作业'''
    response = {}
    try:
        data = request.get_json(force=True)
        job_id = data.get('id')
        scheduler.resume_job(job_id)
        response['message'] = "job[%s] resume success!"%job_id
        response['status'] = True
    except Exception as e:
        response['message'] = str(e)
    return json.dumps(response)

@main.route('/remove',methods=['POST'])
def reomve_jobs():
    '''删除作业'''
    response = {}
    try:
        data = request.get_json(force=True)
        job_id = data.get('id')
        if job_id != 'all':
            scheduler.remove_job(job_id)
            response['message'] = "job[%s] remove success!"%job_id
        else:
            scheduler.remove_all_jobs()
            response['message'] = "job all remove success!"
        response['status'] = True
    except Exception as e:
        response['message'] = str(e)
    return json.dumps(response)

@main.route('/edit', methods=['POST'])
def edit_job():
    '''修改作业'''
    response = {}
    try:
        data = request.get_json(force=True)
        print('data-->',data)
        job_id = data.get('id')
        old_job = scheduler.get_job(job_id)
        if old_job:
            jobfromparm(scheduler,**data)
            response['status'] = True
            response['message'] = "job[%s] edit success!"%job_id
        else:
            response['message'] = "job[%s] Not Found!"%job_id
    except Exception as e:
        response['message'] = str(e)
    return json.dumps(response)

@main.route('/add', methods=['POST'])
def add_job():
    '''新增作业'''
    response = {}
    try:
        data = request.get_json(force=True)
        print('data-->',data)
        job_id = jobfromparm(scheduler,**data)
        response['status'] = True
        response['message'] = "job[%s] add success!"%job_id
    except Exception as e:
        response['message'] = str(e)
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
            info = {
                'id':ret.id,
                'next_run_time':ret.next_run_time,
                'cmd':ret.kwargs.get('cmd'),
                #'func':ret.func_ref,
                'status':'running' if ret.next_run_time != None else 'stop',
                'cron':cron
            }
            inof_list.append(info)
        response['status'] = True
        response['data'] = inof_list
    except Exception as e:
        response['message'] = str(e)
    return json.dumps(response,cls=DateEncoder)

@main.route('/log', methods=['GET'])
def job_log():
    '''获取所有job log信息'''
    response = {}
    try:
        jid = request.args.get('id')
        ret = get_job_logs(jid)
        response['status'] = True
        response['data'] = ret
    except Exception as e:
        response['message'] = str(e)
    return json.dumps(response,cls=DateEncoder)
