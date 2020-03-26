#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 25/03/2020 14:11
# @Author  : Alan
# @Site    : 
# @File    : bootstrap.py
# @Software: PyCharm


class BootstrapFrom(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label)