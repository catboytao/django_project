#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 25/03/2020 15:57
# @Author  : Alan
# @Site    : 
# @File    : draw.py
# @Software: PyCharm

from PIL import Image

img = Image.new(mode='RGB',size=(120,30),color=(255,255,255))

with open('code.png','wb') as f:
    img.save(f,format='png')