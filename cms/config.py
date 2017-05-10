#!/usr/bin/env python2.7
#-*- coding:utf8 -*-

import os

setting = {
    'static': os.path.join(os.path.dirname(__file__), 'static'),
    'template': os.path.join(os.path.dirname(__file__), 'template'),
    'log_path': os.path.join(os.path.dirname(__file__), 'logs'),
    'mem': {
           'host': '106.185.28.67',
           'port': 11211,
           'timeout':30*60
    },
    
    'mongodb' : {
            'host': '106.185.28.67',
            'port': 27017,
            'dbname': 'info',
    },

    'session' : {
        'expires_days': 7,
        'time_out': 90000, #1 * 30 * 60
        'token_time_out': 60, #60s
        'mobile_time_out': 259200, #3d
        'mobile_app_secret': 'myrd@app'
    },
    'domain' : 'http://test.com:8888',
    'static_domain' :'http://test.com:8888',
    'listen_port':8888,
}
