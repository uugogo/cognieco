#usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import pymongo
import socket
import time
import os
import re

socket.setdefaulttimeout(10.0)

dbconn = "106.185.28.67"

Connection = pymongo.Connection(dbconn, 27017)
db = Connection.sinainfo

strtime = time.strftime("%Y", time.localtime())

dbthisyear = db[strtime]
collection = dbthisyear.find({"ContentType" : "news"} , timeout=False).sort([("Date", -1)]).limit(10000)

find_item = re.compile(r'src="(.+?).jpg"', re.DOTALL)

for r in collection:
    Pictures = ""
    #print r["Date"]

    allItems = find_item.findall(r["Content"])

    for item in allItems:

        if len(item) > 120:
            continue

        url = item + ".jpg"
        if not url.startswith("http:"):
	    continue
	imgpath = './img/' + url.replace("http://",'').replace("/",'_')

        try:
            if not os.path.isfile(imgpath):
                print url, imgpath
                urllib.urlretrieve(url, imgpath)
        except IOError as e:
            print e.__str__()
            continue
    #
    # for pic in r['Pictures'] :
    #     url = pic["Url"]
    #     imgpath = './img/' + url.replace("http://",'').replace("/",'_')
    #
    #     try:
    #         if not os.path.isfile(imgpath):
    #             print url, imgpath
    #             urllib.urlretrieve(url, imgpath)
    #     except IOError as e:
    #         print e.__str__()
    #         continue

print 'Done!'
