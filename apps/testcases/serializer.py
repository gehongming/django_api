#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/16 20:25
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm
import json
from rest_framework import serializers
# 继承Serializer类或者 于类
from rest_framework.validators import UniqueValidator
from projects.serializer import ProjectModelSerializer
from testcases.models import TestCases
from utils.validates import where_existed_project_id, where_existed_interface_id, where_existed_env_id
from configures.models import Configures
from projects.models import Projects
from interfaces.models import Interfaces


class InterfacesAnothrSerializer(serializers.ModelSerializer):

    project = serializers.StringRelatedField(help_text='项目名称')
    # 项目ID
    pid = serializers.IntegerField(write_only=True, validators=[where_existed_project_id], help_text='项目ID')
    # 接口ID
    iid = serializers.IntegerField(write_only=True, validators=[where_existed_interface_id], help_text='接口ID')

    class Meta:
        model = Interfaces
        fields = ('iid', 'name', 'project', 'pid')
        extra_kwargs = {
                'name': {
                    'read_only': True
                }
        }

    def validate(self, attrs):
        """
        校验 项目和接口信息是否一致。
        :param attrs:
        :return:
        """
        if not Interfaces.objects.filter(id=attrs['iid'], project_id = attrs['pid'], is_delete=0).exists():
            raise serializers.ValidationError('项目和该接口不匹配')
        return attrs


class TestcasesSerializer(serializers.ModelSerializer):
    """
    用例序列化器
    """
    interface = InterfacesAnothrSerializer(help_text='项目id和接口id')
    class Meta:
        # 指定参考哪一个模型类
        model = TestCases
        exclude = ('update_time', 'create_time', 'is_delete')

        extra_kwargs = {
            'request': {
                'write_only': True
            },
            'include': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        # 用了上面的序列化之后 即使前端传给我id 我这边也是接受到了项目名称。
        interface_dict = validated_data.pop('interface')
        validated_data['interface_id'] = interface_dict['iid']
        interface = TestCases.objects.create(**validated_data)
        return interface

    def update(self, instance, validated_data):
        # 修改和创建一样。
        if 'interface' in validated_data:
            interface_dict = validated_data.pop('interface')
            validated_data['interface_id'] = interface_dict['iid']
        return super().update(instance, validated_data)


class TestcasesRunSerializer(serializers.ModelSerializer):
    """
    运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量id',
                                      validators=[where_existed_env_id])
    class Meta:
        # 指定参考哪一个模型类
        model = TestCases
        # 指定具体字段
        fields = ("id", "env_id")



