#!/usr/bin/env python
#encoding:utf-8
'''
author: yangmingwei
email: yangmingwei@shinezone.com
'''
from . import main

@main.route('/')
def index():
    return 'Index'
