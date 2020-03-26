#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 19/03/2020 18:03
# @Author  : Alan
# @Site    : 
# @File    : schedule.py
# @Software: PyCharm


from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
# 输出时间
from crawler import Crawler



def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    html = Crawler.get_html()
    data = Crawler.parse_html(html)
    print(data)

# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval',minutes=2)
scheduler.start()