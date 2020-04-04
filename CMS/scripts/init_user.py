#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 27/03/2020 9:17
# @Author  : Alan
# @Site    : 
# @File    : init_user.py
# @Software: PyCharm
'''
django 离线脚本
'''

import django
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 导入项目配置
os.environ.setdefault("DJANGO_SETTINGS_MODULE","CMS.settings")
# 模拟启动manage.py
django.setup()

from crm import models
models.User.objects.create(username="Kim",password="12341234",email="912832332@qq.com",phone_num="18235235243")
