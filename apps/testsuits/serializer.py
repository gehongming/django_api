#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/16 20:25
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm


from rest_framework import serializers


# 继承Serializer类或者 于类
from interfaces.models import Interfaces
from projects.models import Projects
from testsuits.models import Testsuits
from utils import validates


class TestsuitsModelSerializer(serializers.ModelSerializer):
    # StringRelatedField 将关联对象（模型类）的指定字段数据进行序列化输出。
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.filter(is_delete=0))

    class Meta:
        # 指定参考哪一个模型类
        model = Testsuits
        exclude = ('is_delete',)

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                 'format': "%Y-%m-%d %H:%M:%S"
            },
            'update_time': {
                'read_only': True,
                'format': "%Y-%m-%d %H:%M:%S"
            }
        }

    def create(self, validated_data):
        # 用了上面的序列化之后 即使前端传给我id 我这边也是接受到了项目名称。
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        interface = Interfaces.objects.create(**validated_data)
        return interface

    def update(self, instance, validated_data):
        # 修改和创建一样。
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
        return super().update(instance, validated_data)


class TestsuitsRunSerializer(serializers.ModelSerializer):

    """
    通过套件运行测试用例
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text="环境变量ID",
                                      validators=[validates.where_existed_env_id])
    class Meta:
        # 指定参考哪一个模型类
        model = Testsuits
        # 指定具体字段
        fields = ("id", "env_id")



