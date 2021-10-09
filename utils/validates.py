#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/10/4 15:35
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm

from rest_framework import serializers

from projects.models import Projects
from interfaces.models import Interfaces
from envs.models import Envs


def where_existed_project_id(value):
    """
    检查项目id是否存在。
    :return:
    """
    if not isinstance(value, int):
        raise serializers.ValidationError('所选项目有错误')
    elif not Projects.objects.filter(is_delete=0, id=value).exists():
        raise serializers.ValidationError('所选项目不存在')


def where_existed_interface_id(value):
    """
    检查项目id是否存在。
    :return:
    """
    if not isinstance(value, int):
        raise serializers.ValidationError('所选接口有错误')
    elif not Interfaces.objects.filter(is_delete=0, id=value).exists():
        raise serializers.ValidationError('所选接口不存在')


def where_existed_env_id(value):
    """
    检查环境id是否存在
    :param value:
    :return:
    """
    if not isinstance(value, int):
        raise serializers.ValidationError('所选接口有错误')
    elif not Envs.objects.filter(is_delete=0, id=value).exists():
        raise serializers.ValidationError('所选接口不存在')

