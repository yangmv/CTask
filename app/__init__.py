#!/usr/bin/env python
#encoding:utf-8
'''
author: yangmingwei
'''
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import fcntl
import atexit

db = SQLAlchemy()
scheduler = APScheduler()

def create_app(config_name):
    app = Flask(__name__)
    #app.config['JSON_AS_ASCII'] = False
    # 进行app配置 把自己的config设定导入到app中
    app.config.from_object(config[config_name])

    # 初始化app配置
    config[config_name].init_app(app)

    db.init_app(app)
    db.app = app

    # 初始化apscheduler,全局锁确保scheduler只运行一次
    f = open("scheduler.lock", "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler.init_app(app)
        scheduler.start()
    except:
        pass
    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
    atexit.register(unlock)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .job import main as job_blueprint
    app.register_blueprint(job_blueprint,url_prefix='/v1/cron/job')

    return app