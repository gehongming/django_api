#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/5 15:44
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm
from django.urls import path

from . import views

urlpatterns = [
    path('summary/', views.SummaryApiView.as_view())
]
