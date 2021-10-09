#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/5 15:44
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm


from django.urls import path, include
from index import views
from rest_framework import routers
# from .views import index

# 1、创建路由对象
# router = routers.SimpleRouter()
router = routers.DefaultRouter()
# 2、注册路由
# 第一个参数 prefix：路由前缀。一般添加为应用名即可。
# 第一个参数 viewset: 视图集类.不要加as_view()
router.register(r'index', views.IndexApiView)

urlpatterns = [
    path('', include(router.urls))
]
