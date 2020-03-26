#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 24/03/2020 15:00
# @Author  : Alan
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.urls import path
from crm.views import account,home

urlpatterns = [
    path('register/', account.register, name='register'),
    path('send_sms/', account.send_sms, name='send_sms'),
    path('login/sms/', account.login_sms, name="login_sms"),
    path('login/', account.login, name="login"),
    path('image/code/', account.image_code, name="image_code"),
    path('articles/', account.formset, name="articles"),
    path('index/',home.index,name="index"),
    path('logout/',account.logout,name="logout"),
]