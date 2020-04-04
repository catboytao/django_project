#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 26/03/2020 20:16
# @Author  : Alan
# @Site    : 
# @File    : auth.py
# @Software: PyCharm
import datetime

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from crm import models


class Tracer(object):

    def __init__(self):
        self.user = None
        self.price_policy = None



class AuthMiddleware(MiddlewareMixin):

    def process_request(self,request):
        '''
        如果用户已登录，则request中赋值
        '''

        tracer_obj = Tracer()

        user_id = request.session.get("user_id",0)
        user_obj = models.User.objects.filter(id=user_id).first()
        tracer_obj.user = user_obj
        #request.tracer = user_obj
        # 白名单，没有登录也可以访问的URL
        '''
        1.获取当前用户访问的URL
        2.检查URL是否在白名单中，如果在则可以继续向后访问，否在判断是否登录
        '''
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        # 检查用户是否登录，已登录继续往后执行，未登录返回登录界面
        if not tracer_obj.user:
            return redirect('crm:login')

        # 获取当前用户拥有的所有额度
        # 获取当前用户ID值最大的交易记录
        transaction_obj = models.Transaction.objects.filter(user=user_obj,status=2).order_by('-id').first()
        # 判断额度是否已过期
        current_datetime = datetime.datetime.now()
        end_datetime = transaction_obj.end_datetime
        # 如果过期 就用免费版
        if end_datetime and  end_datetime < current_datetime:
            transaction_obj = models.Transaction.objects.filter(user=user_obj,price_policy__category=1).first()

        #request.price_policy = transaction_obj.price_policy
        tracer_obj.price_policy = transaction_obj.price_policy
        request.tracer = tracer_obj
