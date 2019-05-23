#!/usr/bin/env python
#encoding:utf-8
'''
author: yangmingwei
email: yangmv@126.com
'''
from . import main

@main.route('/')
def index():
    return 'Index'
