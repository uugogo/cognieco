#!/usr/bin/env python2.7
#-*- coding:utf8 -*-
#
"""
Session class. (Based on Memcached)

Notes:

Memcached以Key-Value方式存储用户数据，key为保存在客户端cookie中的session_id，
Value为用户数据，并允许通过session_id来获取和设置session数据.

Example:

  - Start:
  
  if __name__ == "__main__":
    http_server = HTTPServer(application, xheaders = True)
    if len(sys.argv) >= 2:
        http_server.listen(int(sys.argv[1]))
    else:
        http_server.listen(config.settings['listen_port'])
    #启动Session
    Session.start(config.settings['session']['mc_host'], 
                 config.settings['session']['mc_port'], 
                 config.settings['session']['time_out'])
                 
  - Instance:
  
    session = Session(request)
      
  - SetValue:
  
    session.set('user',user)

  - GetValue:
  
    session.get('user')
  
  - Destroy
    
    session.destroy()
"""
import uuid
import base64
from lib.mem import Mem
import tornado.escape

class Session:
    #Session过期时间（单位：秒）
    _time_out = None
    _expires_days = None
    _request = None
    _session_id = None
    
    def __init__(self, request, time_out = 0, expires_days = None):
        self._request = request
        self._time_out = time_out
        self._expires_days = expires_days
        self._session_id = self._request.get_secure_cookie("SESSIONID", None)
        uri_session_id = self._request.get_argument("SESSIONID", None)
        if uri_session_id is not None \
            and len(uri_session_id.strip()) > 0:
            self._session_id = tornado.escape.native_str(uri_session_id)
            self._request.set_secure_cookie("SESSIONID", self._session_id, expires_days)
        
        if self._session_id is None:
            self._session_id = tornado.escape.native_str(self._generate_session_id())
            self._request.set_secure_cookie("SESSIONID", self._session_id, expires_days)
    
    def get(self, key):
        val = Mem.get(self._session_id)
        if val is not None:
            Mem.set(self._session_id, val, self._time_out)
            if val.has_key(key):
                return val[key]
        return None
        
    def set(self, key, value):
        ret = False
        val = Mem.get(self._session_id)
        if val is None or isinstance(val, dict) == False:
            val = dict()
        val[key] = value
        ret = Mem.set(self._session_id, val, self._time_out)
        return ret
        
    def destroy(self):
        Mem.delete(self._session_id)
    
    def _generate_session_id(self):
        return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

    def get_sessionid(self):
        return self._session_id

    def generate_uuid(self):
        return tornado.escape.native_str(self._generate_session_id())

    def set_sessionid_by_token(self, token_str):
        token_str = tornado.escape.native_str(token_str)
        val = Mem.get(token_str)
        if val is not None and val != 'token':
            self._session_id = val
            self._request.set_secure_cookie("SESSIONID", self._session_id, self._expires_days)
            Mem.delete(token_str)