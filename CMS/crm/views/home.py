#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 26/03/2020 19:51
# @Author  : Alan
# @Site    : 
# @File    : home.py
# @Software: PyCharm
from django.shortcuts import render, redirect


def index(request):
    if request.tracer:
        return render(request,"index.html")
    return redirect("crm:login")




