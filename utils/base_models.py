#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/10/1 18:24
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm

from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间", help_text="修改时间")
    is_delete = models.BooleanField(default=0, verbose_name="逻辑删除", help_text="逻辑删除")

    class Meta:
        # 表示抽象类，用于其他模型来继承，数据库迁移时不会创建ModelBase表
        abstract = True
        verbose_name = "公共字段表"
