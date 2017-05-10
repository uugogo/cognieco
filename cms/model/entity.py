#!/usr/bin/env python2.7
#-*- coding:utf8 -*-
#

from model._base_ import BaseModel

class EntityModel(BaseModel):
    def __init__(self, operator = None, entityid = None):
        self.table = 'entity'
        self.operator = operator
        self.entityid = entityid

    def edit_entity(self,entity):
        sql = "UPDATE entity SET `name` = %(name)s, `alias`= %(alias)s, `address`=%(address)s,`near`=%(near)s, \
                `phone`=%(phone)s,`mobile`=%(mobile)s,\
                `opentime`=%(opentime)s,`creator`=%(creator)s,`type_1`=%(type_1)s,\
                `type_2`=%(type_2)s,`traffic`=%(traffic)s,`lat`=%(lat)s,`lon`=%(lon)s \
                 where entityid=%(entityid)s" 
    
        return self.execute(sql,**entity)
    
    def get_list(self):
        sql = "select * from entity order by entityid"
        entitys = self.get_rows(sql)
        return entitys
    
    def get_my_list(self, uid):
        sql = "select e.* from `entity` e " \
                " where e.creator=%s order by e.entityid"
        entitys = self.get_rows(sql, uid)
        return entitys
    
    def get_emp_access_list(self, empid):
        sql = "select e.* from auth_employee_role er" \
                " left join `entity` e  on er.entity_id=e.entityid " \
                " where er.emp_id=%s" % empid
        entitys = self.get_rows(sql)
        return entitys
    
    def get_access_list(self, uid):
        sql = "select e.* from `entity` e " \
                " left join entity_user eu " \
                " on eu.entity_id=e.entityid where eu.uid=%s order by e.entityid"
        entitys = self.get_rows(sql, uid)
        return entitys
    
    def add_access(self, entityid, uid):
        sql = "insert into entity_user(uid, entity_id) values(%d, %d)" % (uid, entityid)
        self.execute(sql)
    
    def get_detail(self):
        sql = "select e.*, t1.name as type_1name, t2.name as type_2name from `entity` e "  \
                "left join `type` t1 on t1.typeid=e.type_1 " \
                "left join `type` t2 on t2.typeid=e.type_2 " \
                "where e.entityid=%s "
        entity = self.get_one(sql,self.entityid)
        return entity
    
    def get_by_id(self, entityid):
        sql = "select e.entityid, e.name, e.entity_num from `entity` e where e.entityid=%s "
        entity = self.get_one(sql, entityid)
        return entity
    
    def delete(self):
        sql = "delete from entity where  entityid=%s" 
        ret = self.execute(sql,self.entityid)
        return ret
