#!/usr/bin/env python2.7
#-*- coding:utf8 -*-

from tornado.template import Loader
from tornado.web import RequestHandler
import config
import re

from lib.log import Log
from lib.session import Session
from lib.mem import Mem

class BaseHandler(RequestHandler):   
    
    def initialize(self, method = ''):
        #初始化Sesion
        self._session = Session(self, config.setting['session']['time_out'],
                                config.setting['session']['expires_days'])
        self._method = method
        self._cur_entity = None
        #self._passport = Passport(self)

    def get_current_user(self):
        token_str = self.get_argument('token', '')
        if len(token_str) > 0:
            self._session.set_sessionid_by_token(token_str)
        return self._session.get('user')
        

    def check_user_login(self):
        if self._session.get('user') is None:
            return False
        else:
            return True
    
    def generate_token(self):
        token_str = self._session.generate_uuid()
        if Mem.set(token_str, 'token', config.setting['session']['token_time_out']) == False:
            return None
        else:
            return token_str
    
    def get_current_uid(self):
        user = self._session.get('user')
        if user is None:
            return 0
        else:
            return user['uid']
    
    def get_num(self, param, default = 0):
        num =  self.get_argument(param, default)
        if num is None and default is None:
            return None
        else:
            try:
                num = int(num)
                return num
            except Exception, e:
                return default

    def display(self, tpl, **kwargs):
        #self.render(tpl, **kwargs)
        ''' 先用loader来实现，避免每次模板改动要重新启动服务'''
        try:
            loader = Loader(config.setting['template'])
            self.write(loader.load(tpl).generate(**kwargs))
        except Exception,e:
            self.write(str(e))
        except:
            self.write('template error')
        
    def fetch(self, tpl, **kwargs):
        return self.render_string(tpl, **kwargs)
    
    def get(self, *args, **kwargs):
        try:
            self._get(*args, **kwargs)
        except Exception,e:
            Log.error(e)
            self.render('500.htm', next_url=self.request.uri)
    
    def post(self, *args, **kwargs):
        try:
            self._post(*args, **kwargs)
        except Exception,e:
            Log.error(e)
            self.write('Error')
    
    def _get(self, *args, **kwargs):
        pass
    
    def _post(self, *args, **kwargs):
        pass

    def judge_auth(self, perm_token=''):
        
        print  'Auth Methord:'+perm_token
        user = self.get_current_user()
        if user and user['is_admin']==1:
            return True
        if not user or not user.has_key('role') or not user['role'].has_key('perms') or not user['role']['perms'].has_key(perm_token):
            if not self.request.headers.get("X-Requested-With"):
                self.redirect('/auth/fail')
                return False
            else:
                return False
        return True
                
    def set_cur_entity(self, entityid):
        self._cur_entity = entityid
        user = self.get_current_user()
        if user and user['is_admin']==0 and self._cur_entity:
            for role in user['roles']:
                if int(role['entity_id']) == int(self._cur_entity):
                    user['role'] = role
                    user['role']['role_name'] = user['role']['role_name']
            self._session.set('user', user)

    def safe_pager_uri(self):
        uri = self.request.uri;
        uri = re.compile(r"\?ps=[^&]*", re.S).sub('?', uri)
        uri = re.compile(r"\?p=[^&]*", re.S).sub('?', uri)
        uri = re.compile(r"\&ps=[^&]*", re.S).sub('', uri)
        uri = re.compile(r"\&p=[^&]*", re.S).sub('', uri)
        if uri.find('?') < 0:
            uri += '?'
        else:
            uri += '&'
        return uri