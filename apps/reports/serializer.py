#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/16 20:25
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm


from rest_framework import serializers
from datetime import datetime

# 继承Serializer类或者 于类
from rest_framework.validators import UniqueValidator
from .models import Reports


class ReportsSerializer(serializers.ModelSerializer):

    class Meta:
        # 指定参考哪一个模型类
        model = Reports
        exclude = ('update_time','is_delete')

        extra_kwargs = {
            'create_time': {
                'read_only': True,
            },
            'html': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        report_name = validated_data['data']
        validated_data['name'] = report_name + '_' + datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        report  = Reports.objects.create(**validated_data)
        return report

    def update(self, instance, validated_data):
        # 修改和创建一样。
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
        return super().update(instance, validated_data)




