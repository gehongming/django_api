#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/10/2 17:52
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm
import re
from django.db.models import Count

from configures.models import Configures
from interfaces.models import Interfaces
from testcases.models import TestCases
from testsuits.models import Testsuits


def get_count_by_interface(datas):
    data_list = []
    for item in datas:
        mtch = re.search(r'(.*)T(.*)\..?', item["create_time"])
        item["create_time"] = mtch.group(1) + ' ' + mtch.group(2)
        # 查询接口id
        interface_id = item['id']
        # 计算用例数
        testcases_count = TestCases.objects.filter(interface_id=interface_id, is_delete=0).count()
        # 计算 接口下的的配置总数。
        configures_count = Configures.objects.filter(interface_id=interface_id, is_delete=0).count()
        # 数据格式化。
        item['testcases'] = testcases_count
        item['configures'] = configures_count

        data_list.append(item)

    return data_list