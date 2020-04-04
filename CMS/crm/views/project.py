#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 02/04/2020 16:46
# @Author  : Alan
# @Site    : 
# @File    : project.py
# @Software: PyCharm
from django.http import JsonResponse
from django.shortcuts import render

from crm import models
from crm.form.project import ProjectModelForm

def project_list(request):
    '''
    项目列表
    :param request:
    :return:
    '''

    if request.method == 'GET':
        # 获取价格策略
        tracer = request.tracer
        # 获取项目列表:星标、创建 、参与
        project_dict = {'star':[],'my':[],'join':[]}

        my_project_list = models.Project.objects.filter(creator=tracer.user)
        for project in my_project_list:
            if project.star:
                project_dict['star'].append(project)
            else:
                project_dict['my'].append(project)

        join_project_list = models.ProjectUser.objects.filter(user=tracer.user)

        for item in join_project_list:
            if item.star:
                project_dict['star'].append(item.project)
            else:
                project_dict['join'].append(item.project)

        #obj_list = models.ProjectUser.objects.filter(user=tracer.user).value('project')

        form = ProjectModelForm(request=request)
        return render(request,"project_list.html",{"form":form,"project_dict":project_dict})
    form = ProjectModelForm(request,data=request.POST)
    if form.is_valid():
        # 通过验证:项目名 颜色 描述
        form.instance.creator = request.tracer.user
        # 创建项目
        project_obj = form.save()
        return JsonResponse({"status":True,"msg":"添加成功"})
    return JsonResponse({"status":False,"msg":"添加失败","error":form.errors})