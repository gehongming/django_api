#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/10/2 17:52
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm
import re
from datetime import datetime
from django.db.models import Count

from testcases.models import TestCases


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


def get_testcases_by_interfaces_id(ids_list):
    """
    通过接口id 获取用例
    :param ids_list:
    :return:
    """
    one_list = []
    for interface_id in ids_list:
        # vales_list:返回指定的字段，而不是查询集了
        testcases_qs = TestCases.objects.values_list('id', flat=True).\
            filter(interface_id=interface_id, is_delet=0)
        one_list.extend(list(testcases_qs))
    return one_list

