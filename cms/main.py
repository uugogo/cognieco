#!/usr/bin/env python2.7
#-*- coding:utf8 -*-

import sys
import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler

import config

from lib.log import Log
from lib.mem import Mem

import view

urls = [
    (r"/static/(.*)", StaticFileHandler, {"path": config.setting['static']}),
    (r"/", view.index.IndexHandler),
    (r"/new", view.index.IndexHandlerEx),
    (r"/selected", view.index.SelectedHandler),
    (r"/release", view.index.ReleaseHandler),
    (r"/login", view.index.LoginHandler),
    (r"/logout", view.index.LogoutHandler),
    (r"/user/login", view.index.UserLoginHandler),
    (r"/entity/select", view.entity.EntitySelectHandler),
    (r"/entity/unselect", view.entity.EntityUnSelectHandler),
    (r"/entity/top", view.entity.EntityTopHandler),
    (r"/entity/untop", view.entity.EntityUnTopHandler),
    (r"/entity/released", view.entity.EntityReleasedHandler),
    (r"/package", view.package.PackageHandler),
    (r".*", view.index.ErrorHandler)
]

application = Application(
    urls,
    cookie_secret = "qg6iZZuQSSmfKlYKyjB19dr+q9MfcEN7re2VNDEP5Sw=",
    login_url = "/login",
    template_path = config.setting['template'],
    static_path = config.setting['static'],
    debug = True,
    xsrf_cookies = False,#True
    autoescape = None
)
# http://127.0.0.1:8888/
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    Log.start(config.setting['log_path'], Log.DEBUG)
    Mem.start(config.setting['mem']['host'], config.setting['mem']['port'])
    
    http_server = HTTPServer(application, xheaders = True)
    if len(sys.argv) >= 2:
        http_server.listen(int(sys.argv[1]))
    else:
        http_server.listen(config.setting['listen_port'])
    tornado.autoreload.start(IOLoop.instance(), 500)
    IOLoop.instance().start()
    
