#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 03/04/2020 13:44
# @Author  : Alan
# @Site    : 
# @File    : project.py
# @Software: PyCharm
from django.core.exceptions import ValidationError

from crm import models
from crm.form.bootstrap import BootstrapFrom
from django import forms

class ProjectModelForm(BootstrapFrom,forms.ModelForm):

    #desc = forms.CharField(label="项目描述",widget=forms.Textarea())
    color = forms.CharField(label="颜色",widget=forms.RadioSelect)
    class Meta:
        model = models.Project
        fields = ["project_name","color","desc"]
        widgets = {
            'desc':forms.Textarea,
        }

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.reqeust = request

    # 校验项目名
    def clean_project_name(self):
        #校验项目名是否已存在
        name = self.cleaned_data['project_name']
        creator = self.reqeust.tracer.user
        exists = models.Project.objects.filter(project_name=name,creator=creator).exists()
        if exists:
            raise ValidationError("项目名已存在")
        #校验用户是否还有额度创建项目
        price_policy = self.reqeust.tracer.price_policy
        # 当前用户最多能 创建的项目数
        max_num = price_policy.project_num

        # 当前用户已创建的项目数
        count = models.Project.objects.filter(creator=creator).count()

        if count > max_num:
            raise ValidationError("项目个数超限，请购买套餐")

        return name