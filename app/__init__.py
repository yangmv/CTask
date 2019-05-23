#!/usr/bin/env python
#encoding:utf-8
'''
author: yangmingwei
'''
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

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

    # 初始化apscheduler
    scheduler.init_app(app)
    scheduler.start()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .job import main as job_blueprint
    app.register_blueprint(job_blueprint,url_prefix='/v1/cron/job')

    return app