#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 24/03/2020 22:33
# @Author  : Alan
# @Site    : 
# @File    : encrypt.py
# @Software: PyCharm
import hashlib
from django.conf import settings

def md5(string):
    hash_obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    hash_obj.update(string.encode('utf-8'))
    return hash_obj.hexdigest()