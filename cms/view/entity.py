#!/usr/bin/env python2.7
#-*- coding:utf8 -*-
#

from _base_ import BaseHandler
import time
import pymongo
import textwrap

dbconn = "106.185.28.67"
Connection = pymongo.Connection(dbconn, 27017)
db = Connection.sinainfo
strtime = time.strftime("%Y", time.localtime())
dbthisyear = db[strtime]

class EntitySelectHandler(BaseHandler):
    def _post(self):
        newsID = self.get_argument('newsid','')
        if dbthisyear.find_one({"NewsID":newsID}) == None:
            self.write(dict(data="操作失败",status="failed"))
        else:
            dbthisyear.update({"NewsID":newsID},{"$set":{"State":"selected"}})
            self.write(dict(data="操作成功",status="ok"))

class EntityUnSelectHandler(BaseHandler):
    def _post(self):
        newsID = self.get_argument('newsid','')
        if dbthisyear.find_one({"NewsID":newsID}) == None:
            self.write(dict(data="操作失败",status="failed"))
        else:
            dbthisyear.update({"NewsID":newsID},{"$set":{"State":""}})
            self.write(dict(data="操作成功",status="ok"))

class EntityTopHandler(BaseHandler):
    def _post(self):
        newsID = self.get_argument('newsid','')
        if dbthisyear.find_one({"NewsID":newsID}) == None:
            self.write(dict(data="操作失败",status="failed"))
        else:
            dbthisyear.update({"NewsID":newsID},{"$set":{"Top":"yes"}})
            self.write(dict(data="操作成功",status="ok"))

class EntityUnTopHandler(BaseHandler):
    def _post(self):
        newsID = self.get_argument('newsid','')
        if dbthisyear.find_one({"NewsID":newsID}) == None:
            self.write(dict(data="操作失败",status="failed"))
        else:
            dbthisyear.update({"NewsID":newsID},{"$set":{"Top":""}})
            self.write(dict(data="操作成功",status="ok"))
            
class EntityReleasedHandler(BaseHandler):
    def _post(self):
        #多条更新
        dbthisyear.update({"State":"selected"},{"$set":{"State":"released"}},upsert=False, multi=True)
        self.write(dict(data="操作成功",status="ok"))
