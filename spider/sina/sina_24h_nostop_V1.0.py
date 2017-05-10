#usr/bin/env python
# -*- coding: utf-8 -*-

# update
# 详情：增加城市数据
#
# add
# apns：state接口

#import urllib2
import re
#import pymongo
import codecs
import urllib,urllib2,cookielib
import time
import socket
import json
import os
from pymongo import MongoClient

socket.setdefaulttimeout(10.0)

dbconn = "10.154.156.125"

Connection = MongoClient(dbconn, 27017)
#Connection.admin.authenticate("root","123abc")

#Connection = pymongo.Connection(dbconn, 27017)
db = Connection.sinainfo

find_item = re.compile(r'src="(.+?).jpg"', re.DOTALL)

# http://newdiscoveryapi.sinaapp.com/g.php?gid=1&PageNo=6&PageSize=200
list_prefix = "http://newdiscoveryapi.sinaapp.com/g.php?&PageSize=100"

cookiejar = cookielib.CookieJar()
urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))

def timestamp_datetime(value):
    format = '%Y.%m.%d %H:%M'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

def download_img(url):
    try:
        if not os.path.isdir('./img/'):
            os.mkdir('./img/')
        imgpath = './img/' + url.replace("http://",'').replace("/",'_')
        #print imgpath
        if not os.path.isfile(imgpath):
            urllib.urlretrieve(url, imgpath)
    except Exception as e:
        print e.__str__()

def save2db(item=None):
      uid_dic[item['NewsID']] = ""
      item["State"] = ""
      item["Top"] = ""
      print item["Date"],item['NewsID'] #, item["Title"]

      db[strtime].save(item)
      for pic in item['Pictures'] :
        url = pic["Url"]
        download_img(url)

def pack1(datas=None,type=None,groupid=None):
      for item in datas:
          #print item["createtime"]
          #print time.localtime(int(item["createtime"]))
          hours = (time.time() - time.mktime(time.localtime(int(item["createtime"]))))/3600
          if hours > 24 * 3:
             break

          dic_item = {}
          dic_item["ContentType"] = type
          dic_item["Title"] = item["title"]
          dic_item["Source"] = item["media_name"]
          dic_item["Url"] = item["url"]
          dic_item["LongTitle"] = item["title"]
          dic_item["Keywords"] = item["keywords"]
          dic_item["NewsID"] = item["id"]
          dic_item["GroupID"] = groupid
          dic_item["Date"] = timestamp_datetime(int(item["createtime"]))
          dic_item["Pictures"] = []
          dic_item["Content"] = ""

          try:
              detail_url = "http://platform.sina.com.cn/news/news?app_key=2616297505&format=json&url=" + item["url"]
              #print "detail: ",detail_url
              detail = urlOpener.open(detail_url).read()
              detail_data = json.loads(detail)
              detail_content = ""
              for detail_item in detail_data["result"]["data"]:
                 detail_content = detail_item["content"]

                 dic_item["Content"] = detail_content
                 for img in detail_item["images"]:
                     dic_item["Pictures"].append(dict(Url=img["url"]))

              #print dic_item["Title"],dic_item["Url"]

          except Exception,e:
              print "detail: ", e
          if not uid_dic.has_key(dic_item["NewsID"]):
                 save2db(dic_item)

def pack2(datas=None,type=None,groupid=None):
      for item in datas:
          #print item["createtime"]
          #print time.localtime(int(item["createtime"]))

          dic_item = {}
          dic_item["ContentType"] = type
          dic_item["Title"] = item["name"]
          dic_item["Source"] = item["sub_ch"]
          dic_item["Url"] = item["url"]
          dic_item["LongTitle"] = item["short_name"]
          dic_item["Keywords"] = ""
          dic_item["NewsID"] = item["id"]
          dic_item["GroupID"] = groupid
          dic_item["Date"] = item["createtime"]
          dic_item["Content"] = ""

          if item["img_url"] == "":
              dic_item["Pictures"] = []
          else:
              dic_item["Pictures"] = [dict(Url=item["img_url"])]

          dic_item["Content"] = item["short_intro"]

          if not uid_dic.has_key(dic_item["NewsID"]):
                 save2db(dic_item)

def pack9_1(datas=None,type=None,groupid=None):
      for item in datas:
          #print item["createtime"]
          #print time.localtime(int(item["createtime"]))

          dic_item = {}
          dic_item["ContentType"] = type
          dic_item["GroupID"] = groupid
          dic_item["Title"] = item["name"]
          dic_item["Source"] = item["author"]
          dic_item["Url"] = item["url"]
          dic_item["LongTitle"] = item["name"]
          dic_item["Keywords"] = ""
          dic_item["NewsID"] = "HDid" + item["HDid"]
          dic_item["Date"] = timestamp_datetime(int(item["createtime"]))
          dic_item["Content"] = ""

          dic_item["Pictures"] = []

          dic_item["Content"] = item["photo_info"]["script"]

          try:
              detail_url = "http://photo.auto.sina.com.cn/interface/v2/general/get_HD_detail_by_HDid.php?HDid=" + item["HDid"]
              #print "detail: ",detail_url
              detail = urlOpener.open(detail_url).read()
              detail_data = json.loads(detail)
              detail_content = ""
              for detail_item in detail_data["result"]["data"]["photo_list"]:
                 img = detail_item["img"]
                 dic_item["Pictures"].append(dict(Url=img))

          except Exception,e:
              print "detail: ", e
          if not uid_dic.has_key(dic_item["NewsID"]):
                 save2db(dic_item)
def pack9_2(datas=None,type=None,groupid=None):
      for item in datas:
          #print item["createtime"]
          #print time.localtime(int(item["createtime"]))

          dic_item = {}
          dic_item["ContentType"] = type
          dic_item["GroupID"] = groupid
          dic_item["Title"] = item["title"]
          dic_item["Source"] = item["media_name"]
          dic_item["Url"] = item["url"]
          dic_item["LongTitle"] = item["title"]
          dic_item["Keywords"] = ""
          dic_item["NewsID"] = "jaid" + item["id"]
          dic_item["Date"] = item["createdate"] + " " + item["createtime"]
          dic_item["Content"] = item["content"]

          dic_item["Pictures"] = [dict(Url=item["img"])]

          if not uid_dic.has_key(dic_item["NewsID"]):
                 save2db(dic_item)

def fetchNewdiscovery():
    categrey = range(1, 16)
    categrey.append(99)
    for i in categrey:

        #if i not in [3,4,5,8,9,11]:
        if i not in [11]:
            continue
        gid = str(i)

        print "gid: " + gid
        page = 0

        while True:
              uri = list_prefix + "&gid=" + gid + "&PageNo=" + str(page)
              page += 1
              try:
                  #detail = urllib2.urlopen(uri).read()
                  print uri
                  detail = urlOpener.open(uri).read()
                  data = json.loads(detail)
                  #print data
                  #print isinstance(data,'dict')
                  content = data["data"]
                  if content is None:
                      break
                  else:
                      print len(content)
              except:
                  break

              date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
              for item in data["data"]:
                       if not uid_dic.has_key(item["NewsID"]):
                            save2db(item)
                            date = item["Date"]
                       else:
                           break
                           #print item["Title"]
              #print date
              t1 = time.strptime(date, "%Y-%m-%d %H:%M:%S")#2014-06-26 17:41:00
              hours = (time.time() - time.mktime(t1))/3600
              if hours > 23:
                  break

def loadExisted():
    collection = dbthisyear.find()
    print dbthisyear.find().count()
    for row in collection:
        uid_dic[row['NewsID']] = ''


isfirsttime = True
while True:
    strtime = time.strftime("%Y", time.localtime())
    isNotifyTime = time.strftime("%Y.%m.%d %H", time.localtime())
    print "NotifyTime:",isNotifyTime

    uid_dic ={}
    # 8时做爬取，每天一次
    if isfirsttime == True:
        isfirsttime = False
    else:
        if isNotifyTime.endswith("01") \
            or isNotifyTime.endswith("09")\
            or isNotifyTime.endswith("16")\
            or isNotifyTime.endswith("21"): #多了8个小时
            print "start query at: ", isNotifyTime
        else:
            time.sleep(3600)
            continue

    #得到已经保存的数据id
    dbthisyear = db[strtime]
    loadExisted()


    #3 4 5 8 9 11 21 22
    channels = [

        dict(groupid="3", type="股票", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=finance&cat_1==zq1||=mg||=gg&tag=1&page="),
        dict(groupid="3", type="贵金属", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=finance&cat_1=gjs&tag=1&page="),
        dict(groupid="3", type="期货", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=finance&cat_1=qh&tag=1&page="),
        dict(groupid="3", type="债券", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=finance&cat_1=zq2&tag=1&page="),
        dict(groupid="3", type="能源", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=finance&cat_1=ny7&tag=1&page="),

        dict(groupid="4", type="互联网", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=tech&cat_3=tech3_hlwqb&tag=1&format=json&show_num=150"),
        dict(groupid="4", type="电信", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=tech&cat_1=txydx&level==1||=2&tag=1&format=json&show_num=150"),
        dict(groupid="4", type="IT业界", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=tech&cat_1=yj1&level==1||=2&tag=1&format=json&show_num=150"),
        dict(groupid="4", type="数码", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=tech&cat_1=tech3_smxj&&level==1||=2&tag=1&format=json&show_num=150"),
        dict(groupid="4", type="笔记本", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=tech&cat_1=tech3_bjb&&level==1||=2&tag=1&format=json&show_num=150"),

        dict(groupid="5", type="明星八卦", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=ent&cat_1=mxqjc&cat_4==jbbg||=djtp&tag=1&page="),
        dict(groupid="5", type="电影", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=ent&cat_1=dybk&tag=1&page="),
        dict(groupid="5", type="电视", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=ent&cat_1=dsqy&level==2||=3&tag=1&page="),
        dict(groupid="5", type="戏剧", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=ent&cat_1=xj1&tag=1&page="),
        dict(groupid="5", type="音乐", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=ent&cat_1=yl2&tag=1&page="),

        dict(groupid="8", type="高考", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=edu&cat_1=gk&tag=1&page="),
        dict(groupid="8", type="人物对话", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=edu&cat_2=rwdh&tag=1&page="),
        dict(groupid="8", type="出国\留学\移民", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=edu&cat_1==lxcg||=ymdt||=ymgs||=ymms&tag=1&page="),
        dict(groupid="8", type="考研", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=edu&cat_1=ky3&tag=1&page="),
        dict(groupid="8", type="公务员", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=edu&cat_1=ky3&tag=1&page="),
        dict(groupid="8", type="MBA\商学院", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=edu&cat_1=sxy&tag=1&page="),
        dict(groupid="8", type="外语", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=edu&cat_1==zcyy||=syxw||=seyy||=hdjl||=yykt&tag=1&page="),

        dict(groupid="9", type="汽车图片", preurl="http://photo.auto.sina.com.cn/interface/general/get_HD_by_type_recom.php?recom=1&limit=100"),
        dict(groupid="9", type="汽车新闻", preurl="http://data.auto.sina.com.cn/api/wap/get_newslist_top.php?limit=20"),
        
        dict(groupid="11", type="看见", preurl="http://platform.sina.com.cn/slide/album_photo_col?app_key=2616297505&photo_col_id=10&tags=cat&tagmode=any&page="),
        dict(groupid="11", type="记忆", preurl="http://platform.sina.com.cn/slide/album_photo_col?app_key=2616297505&photo_col_id=12&tags=cat&tagmode=any&format=json&page="),
        dict(groupid="11", type="天下", preurl="http://platform.sina.com.cn/slide/album_photo_col?app_key=2616297505&photo_col_id=11&tags=cat&tagmode=any&format=json&page="),
        dict(groupid="11", type="拼图", preurl="http://platform.sina.com.cn/slide/album_photo_col?app_key=2616297505&photo_col_id=9&tags=cat&tagmode=any&format=json&page="),
        dict(groupid="11", type="摄影师", preurl="http://platform.sina.com.cn/slide/album_photo_col?app_key=2616297505&photo_col_id=13&tags=cat&tagmode=any&format=json&page="),

        dict(groupid="21", type="健康", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=health&tag=1&page="),
        dict(groupid="21", type="健康热点", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=health&cat_2=jk-rdxw&tag=1&page="),
        dict(groupid="21", type="养生", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=health&cat_2=ctys&tag=1&page="),
        dict(groupid="21", type="健康新知", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=health&cat_2=jk-jkxz&tag=1&page="),

        dict(groupid="22", type="星座故事", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=other&cat_1=xqxq&tag=1&show_num=130"),
        dict(groupid="22", type="心理", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=other&cat_1==xltm||=xlcs&tag=1&show_num=130"),
        dict(groupid="22", type="运势", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=other&cat_1=ysdjk&tag=1&show_num=130"),
        dict(groupid="22", type="星相教程", preurl="http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=other&cat_1==ssxz||=dlzb||=zxjc||=smls&tag=1&show_num=130"),
    ]

    for i in channels:
        preurl = i["preurl"]
        groupid = i["groupid"]
        type =  i["type"]

        print groupid, type

        page = 1
        while True and page < 10:
            if groupid in ["5", "9", "22"]:
                page = 30
                uri = preurl
            else:
                uri = preurl + str(page)
            print uri
            page += 1
            try:
              #detail = urllib2.urlopen(uri).read()
              list = urlOpener.open(uri).read()
              data = json.loads(list)

              if groupid == "9" and type in ["汽车图片"] :
                  datas = data["data"]
                  pack9_1(datas, type,groupid)
              elif groupid == "9" and type in ["汽车新闻"] :
                  datas = data["result"]["data"]
                  pack9_2(datas, type,groupid)
              elif list.find("result") > 0:
                  datas = data["result"]["data"]

                  if len(datas) == 0:
                      break

                  pack1(datas, type,groupid)
              else:
                  if data["count"] == "0":
                    break
                  datas = data["data"]
                  pack2(datas, type,groupid)

              # print list
              # print type(data)

            except Exception,e:
                print "list: ", e
                break

    fetchNewdiscovery()
    
    collection = dbthisyear.find({} , timeout=False).sort([("Date", -1)]).limit(5000)

    for r in collection:
        Pictures = ""
        print r["Date"]

        Content = ""
        if r.has_key("Content"):
                Content = r['Content']

        allItems = find_item.findall(Content)

        for item in allItems:
            if len(item) > 100:
                continue

            #print item

            url = item + ".jpg"
            if not url.startswith("http:"):
            	  continue
            imgpath = './img/' + url.replace("http://",'').replace("/",'_')

            try:
                if not os.path.isfile(imgpath):
                    #print url, imgpath
                    urllib.urlretrieve(url, imgpath)
            except Exception as e:
                print e.__str__()
                continue

        for pic in r['Pictures'] :
            url = pic["Url"]
            imgpath = './img/' + url.replace("http://",'').replace("/",'_')

            try:
                if not os.path.isfile(imgpath):
                    print url, imgpath
                    urllib.urlretrieve(url, imgpath)
            except Exception as e:
                print e.__str__()
                continue

    print 'Done!   news got at ' + time.strftime("%Y.%m.%d %H:%M", time.localtime())

#21 健康
#http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=health&tag=1&page=1
#http://platform.sina.com.cn/news/news?app_key=2616297505&format=json&url=http://health.sina.com.cn/hc/y/2014-06-26/0744141025.shtml
#22 星座
#http://platform.sina.com.cn/news/news_list?app_key=2616297505&channel=other&cat_1=xqxq&tag=1&page=1
#http://platform.sina.com.cn/news/news?app_key=2616297505&format=json&url=http://health.sina.com.cn/hc/sh/2014-07-04/1547141751.shtml
