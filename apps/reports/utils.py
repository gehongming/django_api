#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/10/2 17:52
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm
import re
from datetime import datetime
from django.db.models import Count


def format_output(datas):
    data_list = []
    for item in datas:
        result = 'Pass' if item['result'] else 'Fail'
        mtch = re.search(r'(.*)T(.*)\..*?', item["create_time"])
        item["create_time"] = mtch.group(1) + ' ' + mtch.group(2)
        # 数据格式化。
        item['result'] = result
        data_list.append(item)
    return data_list


def get_file_contents(filename, chunk_size=512):
    with open(filename, encoding='utf-8') as f:
        while True:
            c =f.read(chunk_size)
            if c:
                yield c
            else:
                break
    return