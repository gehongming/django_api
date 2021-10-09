#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/10/2 17:52
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm
import re
from django.db.models import Count


def handle_env(datas):
    """
    时间格式化
    :param datas:
    :return:
    """
    data_list = []
    for item in datas:
        mtch = re.search(r'(.*)T(.*)\..?', item["create_time"])
        item["create_time"] = mtch.group(1) + ' ' + mtch.group(2)
        data_list.append(item)

    return data_list