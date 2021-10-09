#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/20 14:41
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm
import json
from django.http import HttpResponse, JsonResponse, Http404


# Create your views here.


from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import mixins
from demo1.models import Projects
from demo1.serializer import ProjectSerializer, ProjectModelSerializer

# 我们发现 rest_frameworkh中的mixins.ListModelMixin.业务逻辑和我们的
# ProjectsList代码一致。所以可以直接继承


class ProjectsList(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   GenericAPIView):

    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer

    ordering_fields = ['name', 'leader']
    filterset_fields = ['name', 'tester', 'leader', 'id']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # mixins.CreateModelMixin,中没有try是因为。drf会自动处理异常。
    def post(self, request, *args, **kwargs):
        """新增项目"""
        return self.create(request, *args, **kwargs)


class ProjectsDetail(GenericAPIView,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):

    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer

    # 原本的pk可以用*args, **kwargs 代替。且保持了同意
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
