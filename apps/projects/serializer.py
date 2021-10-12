#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/16 20:25
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm

# 继承Serializer类或者 子类
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from debugtalks.models import DebugTalks
from projects.models import Projects
from interfaces.models import Interfaces
from utils import validates


def is_unique_project_name(name1):
    if '项目' not in name1:
        raise serializers.ValidationError('项目名称必须包含项目')


class ProjectModelSerializer(serializers.ModelSerializer):
    # 当额外定义了一个属性且名称和序列化器的字段名称一致。会覆盖序列化器的字段。
    name = serializers.CharField(
        label='项目名称',
        max_length=50,
        help_text='项目名称',
        validators=[
            UniqueValidator(
                queryset=Projects.objects.all(),
                message='不可以重复'),
            # is_unique_project_name
    ])




    class Meta:
        model = Projects
        exclude = ("update_time","is_delete")

        extra_kwargs = {
            'create_time': {
               'read_only': True
            }
        }

    # 创建project同时 创建一个debug_talk
    def create(self, validated_data):
        project_obj = super().create(validated_data)
        DebugTalks.objects.create(project=project_obj)

        return project_obj


class ProjectNameModelSerializer(serializers.ModelSerializer):

    class Meta:
        # 指定参考哪一个模型类
        model = Projects
        # 指定具体字段
        fields = ("id", "name")


class InterfaceNameSerializer(serializers.ModelSerializer):

    class Meta:
        # 指定参考哪一个模型类
        model = Interfaces
        # 指定具体字段
        fields = ("id", "name", "tester")


class InterfacesByProjectIdSerializer(serializers.ModelSerializer):
    interfaces_set = InterfaceNameSerializer(read_only=True, many=True)

    class Meta:
        # 指定参考哪一个模型类
        model = Projects
        # 指定具体字段
        fields = ("id", "interfaces_set")


class ProjectRunSerializer(serializers.ModelSerializer):
    """
    通过项目运行测试用例序列化器
    """
    env_id = serializers.IntegerField(label="所属环境id", help_text="所属环境id",
                                      validators=[validates.where_existed_env_id])

    class Meta:
        model = Projects
        fields = ('id', 'env_id')