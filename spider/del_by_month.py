#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,datetime,time

while True:
  base_dir = './img/'
  list = os.listdir(base_dir)

  filelist = []
  for i in range(0, len(list)):
    path = os.path.join(base_dir,list[i])
    if os.path.isfile(path):
                filelist.append(list[i])

  for i in range(0, len(filelist)):
    path = os.path.join(base_dir, filelist[i])
    if os.path.isdir(path):
        continue
    timestamp = os.path.getmtime(path)
    #print timestamp
    ts1 = os.stat(path).st_mtime
    #print ts1
    
    date = datetime.datetime.fromtimestamp(timestamp)
    #print list[i],"latest change time:",date.strftime('%Y-%m-%d %H:%M:%S')

    last = datetime.datetime.now() - date
    if last.days > 80:
       print last.days,list[i]
       os.remove('./img/' + list[i])


  time.sleep(7200)
