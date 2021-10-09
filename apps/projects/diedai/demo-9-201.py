#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/20 12:26
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
from demo1.serializer import ProjectSerializer,ProjectModelSerializer


class ProjectsList(mixins.ListModelMixin, GenericAPIView):

    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer

    ordering_fields = ['name', 'leader']
    filterset_fields = ['name', 'tester', 'leader', 'id']

    def get(self, request, *args, **kwargs):

        project_qs = self.get_queryset()
        project_qs = self.filter_queryset(project_qs)
        page = self.paginate_queryset(queryset=project_qs)

        if page:
            serializer = ProjectModelSerializer(instance=page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProjectModelSerializer(instance=project_qs, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """新增项目"""

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(serializer.errors,status=400)

        serializer.save()
        return Response(serializer.data,status=201)


class ProjectsDetail(GenericAPIView):

    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer

    def get(self, request, pk):

        project = self.get_object()
        serializer = self.get_serializer(instance=project,)
        return Response(serializer.data)

    def put(self, request, pk):

        project = self.get_object()
        serializer = self.get_serializer(instance=project, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse(serializer.errors)
        serializer.save()
        return JsonResponse(serializer.data, status=201)

    def delete(self, request, pk):

        project = self.get_object()
        project.delete()
        return JsonResponse(None, safe=False, status=204)