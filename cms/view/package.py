#!/usr/bin/env python2.7
#-*- coding:utf8 -*-
#

from _base_ import BaseHandler

from model.package import PackageModel


class PackageHandler(BaseHandler):
    def _post(self):
        Title = self.get_argument('title','')
        Date  = self.get_argument('date','')

        packmodel = PackageModel()

        packmodel.newpack(Title, Date)

        self.write(dict(data="操作成功",status="ok"))



