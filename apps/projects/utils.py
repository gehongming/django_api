#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/10/2 17:52
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm
import re

from django.db.models import Count

from interfaces.models import Interfaces
from testsuits.models import Testsuits


def get_count_by_project(datas):
    data_list = []
    for item in datas:
        mtch = re.search(r'(.*)T(.*)\..?', item["create_time"])
        item["create_time"] = mtch.group(1) + ' ' + mtch.group(2)
        # 查询id
        project_id = item['id']

        # Count('testcases') 为从表的模型名小写 Count为聚合操作。 testcases=  为聚合别名
        # 返回的是一个列表嵌套字典
        interfaces_testcases_obs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')).\
            filter(project_id=project_id, is_delete=0)
        # 计算 项目下的接口总数。项目和接口本身有外键，但是因为涉及到查询 和接口表有关联表的数据。所以才做了聚合。
        interfaces_count = interfaces_testcases_obs.count()
        # 计算 项目下测试用例的总数
        testcases_count = 0
        for one_dict in interfaces_testcases_obs:
            testcases_count += one_dict['testcases']

        # 计算 项目下的配置总数。
        interfaces_configures_obs = Interfaces.objects.values('id').annotate(configures=Count('configures')).\
            filter(project_id=project_id, is_delete=0)
        configures_count = 0
        for one_dict in interfaces_configures_obs:
            configures_count += one_dict['configures']

        # 计算项目下的 testsuits.因为有外键 所以直接查
        testsuits_counts = Testsuits.objects.filter(project_id=project_id, is_delete=0).count()
        # 数据格式化。
        item['interfaces'] = interfaces_count
        item['testcases'] = testcases_count
        item['testsuits'] = testsuits_counts
        item['configures'] = configures_count

        data_list.append(item)

    return data_list