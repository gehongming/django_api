#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/20 15:15
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm
import json
from django.http import HttpResponse, JsonResponse, Http404


# Create your views here.



from demo1.models import Projects
from demo1.serializer import ProjectSerializer, ProjectModelSerializer
from rest_framework import generics



class ProjectsList(generics.ListCreateAPIView):

    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer

    ordering_fields = ['name', 'leader']
    filterset_fields = ['name', 'tester', 'leader', 'id']


class ProjectsDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer


