#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/16 20:25
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm

from rest_framework import serializers

# 继承Serializer类或者 于类
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.settings import api_settings


def is_unique_project_name(name1):
    if '项目' not in name1:
        raise serializers.ValidationError('项目名称必须包含项目')


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(label='确认密码',
                                             min_length=6,
                                             max_length=20,
                                             write_only=True,
                                             help_text='确认密码',
                                             error_messages={
                                                 'min_length': '仅允许6-20个字符的密码',
                                                 'max_length': '仅允许6-20个字符的密码'})
    token = serializers.CharField(label='token',
                                  read_only=True)

    class Meta:
        # django自带的model
        model = User
        # 指定模型类的字段,来生成序列化器
        fields = ('username', 'id', 'password', 'email', 'password_confirm', 'token')

        # 设置字段属性
        # 只能字典嵌套字典.字段名称为key。
        extra_kwargs = {
            'username': {
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许6-20个字符的用户名',
                    'max_length': '仅允许6-20个字符的用户名'
                },
                'validators': {
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message='用户名不可以重复'),
                }
        },
            'email': {
                'label': '邮箱',
                'help_text': '邮箱',
                'write_only': True,
                # 必填。
                'required': True,
                'validators': {
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message='email不可以重复'),}
            },
            'password': {
                'label': '密码',
                'help_text': '密码',
                'write_only': True,
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许6-20个字符的密码',
                    'max_length': '仅允许6-20个字符的密码',
                }
            }
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError('密码不一致')
        return attrs

    def create(self, validated_data):
        # 去除不需要的字段
        validated_data.pop('password_confirm')
        # 第一种保存数据方式：调用父类保存数据
        # user = super(RegisterSerializer, self).create(**validated_data)
        # # 加密密码
        # user.set_password(validated_data['password'])
        # user.save()
        # 第二种保存数据方式，直接使用django-User模型类中的create_user
        user = User.objects.create_user(**validated_data)


        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user



