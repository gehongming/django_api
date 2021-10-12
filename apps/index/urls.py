#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/5 15:44
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm
from django.conf.urls import url
from django.urls import path, include
from index import views
from rest_framework import routers
# from .views import index

urlpatterns = [
    url(r'^baseapi/', include("baseapp.urls")),
    url(r'^.*?$',views.index,name="index"),
]