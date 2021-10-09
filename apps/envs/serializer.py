#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/16 20:25
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm


from rest_framework import serializers
# 继承Serializer类或者 于类
from rest_framework.validators import UniqueValidator
from envs.models import Envs


class EnvsModelSerializer(serializers.ModelSerializer):

    class Meta:
        # 指定参考哪一个模型类
        model = Envs
        exclude = ('update_time','is_delete')

        extra_kwargs = {
            'create_time': {
                'read_only': True
            }
        }


class EnvNameSerializer(serializers.ModelSerializer):

    class Meta:
        # 指定参考哪一个模型类
        model = Envs
        # 指定具体字段
        fields = ("id", "name")



