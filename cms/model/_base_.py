#!/usr/bin/env python2.7
#-*- coding:utf8 -*-
#

from lib.log import Log
from lib.mem import Mem
import functools
import time

"""
"""

def debug_db(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if isinstance(self, BaseModel) == False:
            return method(self, *args, **kwargs)
        else:
            start = time.clock()
            ret = method(self, *args, **kwargs)
            finsh = time.clock()
            BaseModel.set_debug_info((finsh - start) * 1000)
            if self._debug_flag == True and isinstance(args, tuple) and len(args) > 0:
                Log.debug('SQL-Time: %s[%.3fms]', args[0], (finsh - start) * 1000)
            return ret
    return wrapper

class BaseModel():
    _db = None
    _sql_num = 0
    _sql_time = 0
    _debug_flag = False

    @classmethod
    def set_debug_info(cls, sql_time):
        cls._sql_num += 1
        cls._sql_time += sql_time

    @classmethod
    def get_debug_info(cls):
        return (cls._sql_num, cls._sql_time)

    @debug_db
    def get_one(self, sql, *parameters, **kwparameters):
        row = None
        try:
            row = self._db.get(sql, *parameters, **kwparameters)
        except Exception, e:
            Log.warning('Mysql get one error(%s)(%s)', sql, str(e))
        return row
    
    @debug_db
    def get_rows(self, sql, *parameters, **kwparameters):
        rows = None
        try:
            rows = self._db.query(sql, *parameters, **kwparameters)
        except Exception, e:
            Log.warning('Mysql get rows error(%s)(%s)', sql, str(e))
        return rows
    
    @debug_db
    def execute(self, sql, *parameters, **kwparameters):
        ret = [False, 0]
        try:
            ret[1] = self._db.execute_lastrowid(sql, *parameters, **kwparameters)
            ret[0] = True
        except Exception, e:
            Log.warning('Mysql execute error(%s)(%s)', sql, str(e))
        return ret
    
    @debug_db
    def update(self, sql, *parameters, **kwparameters):
        ret = [False, 0]
        try:
            ret[1] = self._db.execute_rowcount(sql, *parameters, **kwparameters)
            ret[0] = True
        except Exception, e:
            Log.warning('Mysql update error(%s)(%s)', sql, str(e))
        return ret
    
    def set_cache(self, key, val, time_out):
        return Mem.set(key, val, time_out)

    def get_cache(self, key):
        return Mem.get(key)
    
    def clear_cache(self, key):
        Mem.delete(key)
    