#!/usr/bin/env python
#encoding:utf-8
import pickle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import datetime
from datetime import date

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def get_jobs():
    engine = create_engine("mysql+pymysql://root:chaBUljXrcyn74F@172.16.0.121:3306/stask?charset=utf8", max_overflow=5)
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    #sql = 'select job_state from apscheduler_jobs WHERE id="test01"'
    sql = 'select id,next_run_time,job_state from apscheduler_jobs'
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
    ret2 = json.dumps(ret,cls=DateEncoder)
    print(ret2)
    # print(json.dumps(result,cls=DateEncoder))
    # for k,v in result.items():
    #     print('[%s]'%k,v)

get_jobs()