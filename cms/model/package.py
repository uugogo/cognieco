#usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import time
import os
import shutil
import json
import re
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class PackageModel():
    def __init__(self):
        self.dbconn = "106.185.28.67"

    def newpack(self, packTitle = "",packDate = ""):
        find_item = re.compile(r'src="(.+?).jpg"', re.DOTALL)

        dbdir = time.strftime("/home/search/spider/product/%Y%m%d%H%M%S/", time.localtime())
        isNotifyTime = time.strftime("%Y.%m.%d %H", time.localtime())

        Connection = pymongo.Connection(self.dbconn, 27017)
        db = Connection.sinainfo
        strtime = time.strftime("%Y", time.localtime())
        dbproduct = db["product"]

        if not os.path.isdir(dbdir):
                os.mkdir(dbdir)

        dbthisyear = db[strtime]
        collection = dbthisyear.find({"State":"selected"} , timeout=False).sort([("Date", -1)]) #"ContentType" : "news",

        pic_id = 0
        jsonout = []

        for r in collection:

            Content = ""

            if r.has_key("Content"):
                Content = str(r['Content'])

            allItems = find_item.findall(Content)
            for item in allItems:
                if len(item) > 120:
                    continue
                url = item + ".jpg"
                pic_id += 1
                pic_name = str(pic_id)+".jpg"
                imgpath = '/home/search/spider/img/' + url.replace("http://",'').replace("/",'_')
                imgoutput = dbdir + pic_name
                try:
                    shutil.copyfile(imgpath, imgoutput)
                except IOError as e:
                    print e.__str__()

                Content = Content.replace('src="'+ url, 'datasrc="'+ pic_name + '" src="')

            Pictures = ""
            for pic in r['Pictures'] :
                pic_id += 1
                pic_name = str(pic_id)+".jpg"
                Pictures += pic_name + "|"
                imgpath = '/home/search/spider/img/' + pic["Url"].replace("http://",'').replace("/",'_')
                imgoutput = dbdir + pic_name
                try:
                    shutil.copyfile(imgpath, imgoutput)
                except IOError as e:
                    print e.__str__()

            js = dict(NewsID = r['NewsID'],
                    GroupID = r['GroupID'],
                    Title = r['Title'],
                    LongTitle = r['LongTitle'],
                    Source = r['Source'],
                    Date = r['Date'],
                    Content = Content,
                    Top = r['Top'],
                    Pictures = Pictures)

            jsonout.append(js)

        # with open(dbdir + 'info.js', 'w') as f:
        #     f.write("var cubedata=" + unicode(json.dumps(jsonout), 'UTF-8'))
        f = codecs.open(dbdir + 'info.js','a','utf-8')
        f.write(u"var cubedata=" + json.dumps(jsonout, ensure_ascii=False))
        f.close()

        filename = time.strftime("%Y%m%d%H%M.zip", time.localtime())
        os.popen("zip -rj /home/search/cms/static/" + filename + " " + dbdir + "*")

        data={}
        data["title"] = packTitle
        data["date"] = packDate
        data["url"] = "http://li728-67.members.linode.com:8888/static/" + filename

        dbproduct.save(data)
