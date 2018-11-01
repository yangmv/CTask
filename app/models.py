#!/usr/bin/env python
#encoding:utf-8
'''
author: yangmingwei
'''
from . import db
from datetime import datetime

class TaskLog(db.Model):
    __tablename__ = 'task_log'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(16))
    status = db.Column(db.Boolean)
    exe_time = db.Column(db.DateTime, default=datetime.now)
    cmd = db.Column(db.String(128))
    stdout = db.Column(db.Text)

    def to_json(self):
        json_post = {
            'id': self.id,
            'task_id': self.task_id,
            'status': self.status,
            #'exe_time': datetime.strftime(self.exe_time, '%Y-%m-%d'),
            'exe_time': self.exe_time,
            'cmd': self.cmd,
            'stdout': self.stdout
        }
        return json_post