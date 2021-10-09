#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/16 20:25
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm


from rest_framework import serializers
# 继承Serializer类或者 于类
from rest_framework.validators import UniqueValidator
from debugtalks.models import DebugTalks


class DebugTalksSerializer(serializers.ModelSerializer):

    project = serializers.StringRelatedField(help_text='项目名称')
    class Meta:
        # 指定参考哪一个模型类
        model = DebugTalks
        exclude = ('create_time', 'update_time', 'is_delete')
        read_only_fields = ("name","project")
        extra_kwargs = {
            'debugtalk': {
                'write_only': True
            }
        }
