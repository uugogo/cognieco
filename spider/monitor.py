#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import time

#导入smtplib和MIMEText
import smtplib,sys 
from email.mime.text import MIMEText

dbconn = "106.185.28.67"

Connection = pymongo.Connection(dbconn, 27017)
db = Connection.sinainfo

def send_mail(sub,content): 
#############
#要发给谁，这里发给1个人
    mailto_list=["zhoumeng@foxmail.com","18133192@qq.com"] 
#####################
#设置服务器，用户名、口令以及邮箱的后缀
    mail_host="smtp.qq.com"
    mail_user="2982020036"
    mail_pass="123abc"
    mail_postfix="qq.com"
######################
    '''''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@126.com","sub","content")
    '''
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_charset='gbk') 
    msg['Subject'] = sub 
    msg['From'] = me 
    msg['To'] = ";".join(mailto_list) 
    try: 
        s = smtplib.SMTP() 
        s.connect(mail_host) 
        s.login(mail_user,mail_pass) 
        s.sendmail(me, mailto_list, msg.as_string()) 
        s.close() 
        return True
    except Exception, e: 
        print str(e) 
        return False
    
if __name__ == '__main__':
    while True:
        strtime = time.strftime("%Y", time.localtime())
        dbthisyear = db[strtime]
        collection = dbthisyear.find({} , timeout=False).sort([("Date", -1)]).limit(1)

        for r in collection:
          hours = (time.time() - time.mktime(time.strptime(r["Date"], '%Y.%m.%d %H:%M')) )/3600
          print "hours:",hours
          if hours > 24 * 3:
            if send_mail(u'数据更新滞后警报',u'监控进程发现数据已经超过3天没有更新了，\n 请及时确认'): 
                print u'发送成功'
            else: 
                print u'发送失败'
        time.sleep(7200)
