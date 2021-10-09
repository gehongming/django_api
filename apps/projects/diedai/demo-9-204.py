#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/20 16:23
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm
import json
from django.http import HttpResponse, JsonResponse, Http404


# Create your views here.
from rest_framework.response import Response

from demo1.models import Projects
from demo1.serializer import ProjectSerializer, ProjectModelSerializer

from rest_framework import viewsets, mixins, status


# viewsets.ViewSet 不支持定义get等方法。只支持action动作。
class ProjectsViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin):

    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer

    ordering_fields = ['name', 'leader']
    filterset_fields = ['name', 'tester', 'leader', 'id']

    # ListModelMixin
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # RetrieveModelMixin
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # UpdateModelMixin
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    # DestroyModelMixin
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # CreateModelMixin
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


