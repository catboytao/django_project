#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 03/04/2020 10:37
# @Author  : Alan
# @Site    : 
# @File    : redis_helper.py
# @Software: PyCharm
from django_redis import get_redis_connection


def insert():
    try:
        conn = get_redis_connection('default')
        conn.set('18223176663','121432',ex=1000)
    except Exception as e:
        print(e)

def get_val():
    value = None
    try:
        conn = get_redis_connection('default')
        value = conn.get('18223176663')
    except Exception as e:
        print(e)
    return value

if __name__ == '__main__':
    #insert()
    value = get_val()
    print(value)
