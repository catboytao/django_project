#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 26/03/2020 13:39
# @Author  : Alan
# @Site    : 
# @File    : formsetDemo.py
# @Software: PyCharm

from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(label="标题")
    pub_date = forms.DateField(label="发布时间")

from django.forms import formset_factory
ArticleFormSet = formset_factory(ArticleForm)


