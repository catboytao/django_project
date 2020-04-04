#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 02/04/2020 16:23
# @Author  : Alan
# @Site    : 
# @File    : base.py
# @Software: PyCharm
import django
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 导入项目配置
os.environ.setdefault("DJANGO_SETTINGS_MODULE","CMS.settings")
# 模拟启动manage.py
django.setup()