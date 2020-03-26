#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 19/03/2020 19:00
# @Author  : Alan
# @Site    : 
# @File    : load_data.py
# @Software: PyCharm
import pymysql

class Loader():

    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="199786",
            database="testdb",
            charset="utf8"
        )
        self.cursor = self.conn.cursor()



    def insert_data(self,data:tuple):
        query = '''
            insert into sports(id,start_time,categroy,project,contest,link) values(?,?,?,?,?,?)
        '''

        self.cursor.execute(query,data)
