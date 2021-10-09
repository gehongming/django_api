#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/5 15:44
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm


from django.urls import path, include
from projects import views
from rest_framework import routers
# from .views import index

# 1、创建路由对象
# router = routers.SimpleRouter()
router = routers.DefaultRouter()
# 2、注册路由
# 第一个参数 prefix：路由前缀。一般添加为应用名即可。
# 第一个参数 viewset: 视图集类.不要加as_view()
router.register(r'projects', views.ProjectsViewSet)

urlpatterns = [
    # path('', views.index),
    # path('', views.IndexView.as_view()),
    # path('<int:pk>/', views.IndexView.as_view()),
    # int为路径参数类型转化器。如果参数为str就无法匹配.pk为参数别名
    # 转换器:int\slug\uuid(唯一标识符)\
    # path('', views.ProjectsList.as_view()),
    # path('<int:pk>/', views.ProjectsDetail.as_view())


    # path('projects/', views.ProjectsViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create',
    # }), name='project-list'),
    # path('projects/<int:pk>/',views.ProjectsViewSet.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'delete': 'destroy'
    # })),
    # path('projects/names/', views.ProjectsViewSet.as_view({
    #     'get': 'names',
    # }), name='project-names'),
    # path('projects/<int:pk>/interfaces/', views.ProjectsViewSet.as_view({
    #     'get': 'interfaces',
    # })),
    # 第一种:将自动生成的路由，添加到urlpatterns
    path('', include(router.urls))
]

# 第二种：
# urlpatterns += router.urls