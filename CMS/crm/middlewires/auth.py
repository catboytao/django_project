#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 26/03/2020 20:16
# @Author  : Alan
# @Site    : 
# @File    : auth.py
# @Software: PyCharm
from django.utils.deprecation import MiddlewareMixin

from crm import models


class AuthMiddleware(MiddlewareMixin):

    def process_request(self,request):
        '''
        如果用户已登录，则request中赋值
        '''

        user_id = request.session.get("user_id",0)
        user_obj = models.User.objects.filter(id=user_id).first()
        request.tracer = user_obj
