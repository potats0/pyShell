#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import os

import records


class db(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(db, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.initialize()

    def initialize(self):
        if not os.path.exists("shell.db"):
            self.db = records.Database('sqlite:///shell.db', connect_args={'check_same_thread': False})
            self.db.query('DROP TABLE IF EXISTS shell')
            self.db.query(
                'CREATE TABLE shell (id INTEGER PRIMARY KEY autoincrement,types text,shell text, passwd text, config text ,remark text, typeid text,coding text,createdtime text,updatetime,text)')
        else:
            self.db = records.Database('sqlite:///shell.db', connect_args={'check_same_thread': False})

    def insert(self, types, shell, passwd, config, remark, typeid, coding, createdtime, updatetime):
        """
    insert()每个参数的含义（从左到右依次）
    types：shell的类型，大写字符串 PHP/ASP/ASPX/CUSTOMER
    shell：shell的地址（记得添加http://)
    passwd：shell的密码
    config：shell的配置，目前留空（空字符串）
    remark：shell的备注
    type_id：目前为"0"
    coding：shell的编码，默认utf-8
    createdtime：shell创建日期 字符串类型 time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    updatetime：shell更新日期，目前暂时和createdtime一致即可
        :return:
        """
        self.db.query(
            'INSERT INTO shell (types, shell, passwd,config ,remark,typeid,coding,createdtime, updatetime) VALUES(:types,:shell, :passwd,:config,:remark,:typeid,:coding,:createdtime,:updatetime)',
            types=types, shell=shell, passwd=passwd, config=config, remark=remark, typeid=typeid, coding=coding,
            createdtime=createdtime, updatetime=updatetime)
        return \
            self.db.query("select * from shell where createdtime=:createdtime and shell=:shell",
                          createdtime=createdtime,
                          shell=shell)[0].id

    def getall(self):
        return self.db.query("select * from shell")

    def delete(self, id):
        '''

        :param id: int
        :return:
        '''
        return self.db.query("delete from shell where id=:id", id=id)

    def get(self, id):
        return self.db.query("select * from shell where id=:id", id=id)[0]
