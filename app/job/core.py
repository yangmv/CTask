#!/usr/bin/env python
#encoding:utf-8
from app.public import exec_shell
from app.models import TaskLog
from app import db

def exe_cmd(cmd,task_id):
    '''执行CMD命令'''
    recode, stdout = exec_shell(cmd)
    data = dict(
        task_id = task_id,
        status = True if recode == 0 else False,
        cmd = cmd,
        stdout = stdout
    )
    new_log = TaskLog(**data)
    db.session.add(new_log)
    db.session.commit()

    if recode != 0:
        print('[Error] (%s) failed'%cmd)
        exit(407)
    print('[Success] (%s) success'%cmd)
    return stdout

def jobfromparm(scheduler,**jobargs):
    id = jobargs['id']
    func=__name__+':'+'exe_cmd'
    args = jobargs['cmd']
    cron = jobargs['cron'].split(' ')
    cron_rel = dict(second=cron[0], minute=cron[1], hour=cron[2], day=cron[3], month=cron[4], day_of_week=cron[5])
    #print('[add job]: ',id)
    scheduler.add_job(func=func,id=id, kwargs={'cmd':args,'task_id':id},trigger='cron',**cron_rel,replace_existing=True)
    #print('[add job ok]')
    return id

def get_job_logs(args):
    jid = args.get('id')
    pageNum = int(args.get('pageNum',1))
    pageSize = int(args.get('pageSize',25))
    if jid == None:
        data_list = TaskLog.query.order_by(TaskLog.id.desc()).paginate(
            pageNum, pageSize, error_out=False
        )
        total = data_list.total
        data_list = data_list.items
    else:
        data_list = TaskLog.query.filter_by(task_id=jid).all()
    ret_list = []
    for data in data_list:
        ret_list.append(data.to_json())
    return ret_list
