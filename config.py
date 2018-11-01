#!/usr/bin/env python
#encoding:utf-8
import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
basedir = os.path.abspath(os.path.dirname(__file__))

###Mysql配置
mysql_info = dict(
    host = '172.16.0.121',
    port = 3306,
    dbname = 'stask',
    username = 'root',
    password = 'chaBUljXrcyn74F'
)

MYSQL_URL = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8'%(mysql_info['username'],mysql_info['password'],
                                                           mysql_info['host'],mysql_info['port'],mysql_info['dbname'])
class Config:
    """基础配置，导入所有配置中"""
    # 数据库自动提交数据
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
    # 这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询耗时过长的时间
    SLOW_DB_QUERY_TIME = 0.5

    # 邮件信息
    MAIL_SUBJECT_PREFIX = '<任务系统>'
    MAIL_SENDER = '任务系统 <it@xxx.com>'
    MAIL_PORT = 465
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'ops@xxx.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '123456'

    # apscheduler 配置信息
    JOBS = [ ]
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=MYSQL_URL)
    }
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 5
    }
    SCHEDULER_API_ENABLED = True

    # 配置类可以定义 init_app() 类方法，其参数是程序实例。
    # 在这个方法中，可以执行对当前 环境的配置初始化。
    # 现在，基类 Config 中的 init_app() 方法为空。
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """开发配置 以及开发时使用的数据库地址"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = MYSQL_URL
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    # @classmethod
    # def init_app(cls, app):
    #     Config.init_app(app)
    #     print('[This is Develoment...]')

class TestingConfig(Config):
    """测试配置 以及测试时使用的数据库地址"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    """正常使用时的配置 以及数据库地址 发生错误时自动发送邮件"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
         'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}