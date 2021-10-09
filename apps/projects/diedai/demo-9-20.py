#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/20 11:52
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm

import json

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.models import Projects
from projects.serializer import ProjectSerializer,ProjectModelSerializer
from interfaces.models import Interfaces
from utils.pagination import PageNumberPaginationManual

# def index(request):
#     """
#     index shitu
#     :return:
#     """
#     if request.method == 'GET':
#         return HttpResponse("<h1>get请求：hello world</h1>")
#     elif request.method == 'POST':
#         return HttpResponse("<h1>post请求：hello world</h1>")
#     else:
#         return HttpResponse("<h1>其他请求：hello world</h1>")


# class IndexView(View):
#
#     # def get(self, request):
#     #     # get请求
#     #     # return render(request, 'index-new.html')
#     #     data = [
#     #         {'name': "京东方", 'leader': "PDD", 'app_name': "P2P"},
#     #         {'name': "把宝来", 'leader': "PDD", 'app_name': "P2P"},
#     #         {'name': "富士康", 'leader': "PDD", 'app_name': "P2P"},
#     #     ]
#     #     return render(request, 'index-new.html', locals())
#     # def get(self, request, pk):
#     #     return HttpResponse("<h1>post请求：hello world</h1>")
#
#     # def post(self, request):
#     #     return HttpResponse("<h1>post请求：hello world</h1>")
#
#     def get(self, request, pk):
#         data = {
#             'name': 'ghm',
#             'age': 14
#         }
#         return JsonResponse(data=data)
#
#     def put(self, request):
#         return HttpResponse("<h1>put请求：hello world</h1>")


# class ProjectView(View):
#
#    def get(self,request):
#        # #  创建模型类对象
#        # one_obj = Projects(
#        #     name='这是一个牛逼的项目',
#        #     leader='icon',
#        #     tester='ghm',
#        #     programer='妞妞',
#        #     publish_app='代码新建项目')
#        # # 调用save 方法保存。
#        # one_obj.save()
#        # Projects.objects.create(
#        #     name='这是一个牛逼的项目2',
#        #     leader='icon',
#        #     tester='ghm',
#        #     programer='妞妞',
#        #     publish_app='代码新建项目'
#        # )
#
#        # 获取数据的所有记录
#        # Projects.objects.all()
#        # 获取指定的记录
#        # one_project = Projects.objects.get(id=1)
#        one_project = Interfaces.objects.filter(projects__name__contains='登录接口')
#
#        pass
#        return JsonResponse()

# class ProjectsList(View):
#
#     def get(self, request):
#         # 1、先获取所有项目信息
#         project_qs = Projects.objects.all()
#
#         # 2、将数据库模型实例化。转化为字典类型（json数组。嵌套字典的列表）
#         project_list = []
#         for project in project_qs:
#             one_dict = {
#                 'name': project.name,
#                 'leader': project.leader,
#                 'tester': project.tester,
#                 'programer': project.programer,
#                 'publish_app': project.publish_app,
#                 'desc': project.desc
#
#             }
#             project_list.append(one_dict)
#
#         return JsonResponse(project_list, safe=False)
#
#     def post(self, request):
#         """新增项目"""
#
#         #  1、从前端获取json格式的数据，转换为python当中的类型
#         # 为了严谨性，这更需要做各种复杂的检验
#         # 比如: 是否为json.传递的项目数据是否符合要求、 有些必传参数是否携带等
#         json_data = request.body.decode('utf-8')
#         python_data = json.loads(json_data, encoding='utf-8')
#
#         # 2、向数据库中新增项目
#         # project = Projects.objects.create(name=python_data['name'],
#         #                         leader=python_data['leader'],
#         #                         tester=python_data['tester'],
#         #                         programer=python_data['programer'],
#         #                         publish_app=python_data['publish_app'],
#         #                         desc=python_data['desc'])
#         # 字典格式使用 **解包
#         project = Projects.objects.create(**python_data, status=201)
#
#         # 3、将模型类转化为字典的格式类型。然后返回。
#         one_dict = {
#             'name': project.name,
#             'leader': project.leader,
#             'tester': project.tester,
#             'programer': project.programer,
#             'publish_app': project.publish_app,
#             'desc': project.desc
#         }
#         return JsonResponse(one_dict)


# class ProjectsDetail(View):
#
#     def get(self, request, id):
#         # 1、校验前端传递的pk值是否存在。类型是否正确，在数据库中是否存在
#         # 2、获取pk值的项目
#         project = Projects.objects.get(id=id)
#         # 3、将模型类对象转换为字典，并返回
#         one_dict = {
#             'name': project.name,
#             'leader': project.leader,
#             'tester': project.tester,
#             'programer': project.programer,
#             'publish_app': project.publish_app,
#             'desc': project.desc
#         }
#         return JsonResponse(one_dict)
#
#     def put(self, request, id):
#
#         # 1、校验前端传递的pk值是否存在。类型是否正确，在数据库中是否存在
#         # 2、获取pk值的项目
#
#         project = Projects.objects.get(id=id)
#         # 从前端获取值，并做校验
#         json_data = request.body.decode('utf-8')
#         python_data = json.loads(json_data, encoding='utf-8')
#         # 4、更新项目
#         project.name = python_data['name']
#         project.leader = python_data['leader']
#         project.tester = python_data['tester']
#         project.programer = python_data['programer']
#         project.publish_app = python_data['publish_app']
#         project.desc = python_data['desc']
#
#         project.save()
#         # 5、将模型类对象转换为字典，并返回
#         one_dict = {
#             'name': project.name,
#             'leader': project.leader,
#             'tester': project.tester,
#             'programer': project.programer,
#             'publish_app': project.publish_app,
#             'desc': project.desc
#         }
#         return JsonResponse(one_dict, status=201)
#
#     def delete(self, request, id):
#         # 1、校验前端传递的pk值是否存在。类型是否正确，在数据库中是否存在
#         # 2、获取pk值的项目
#         project = Projects.objects.get(id=id)
#         project.delete()
#         return JsonResponse(None, safe=False, status=204)


class ProjectsList(GenericAPIView):

# class ProjectsList(APIView):
    # 必须指定queryset 和 serializer_class
    # queryset 用于指定需要使用的查询集
    queryset = Projects.objects.all()
    # serializer_class 用于指定需要使用的序列化器
    serializer_class = ProjectModelSerializer

    # from rest_framework import filters
    # 在视图类中指定过滤引擎---排序
    # filter_backends = [filters.OrderingFilter]
    # 指定需要排序的字段
    ordering_fields = ['name', 'leader']
    # 在视图类中指定过滤引擎---过滤
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'tester', 'leader', 'id']

    pagination_class = PageNumberPaginationManual
    def get(self, request):
        # 1、先获取所有项目信息
        # project_qs = Projects.objects.all()
        # 获取查询集---------有排序的时候只能使用这个。
        project_qs = self.get_queryset()
        # 使用filter_queryset方法过滤查询
        project_qs = self.filter_queryset(project_qs)
        # 使用paginate_queryset来进行分页，要指定查询集且为过滤后的。
        page = self.paginate_queryset(queryset=project_qs)
        if page:
            # 如果配置了分页，page返回不为空。就走这个逻辑
            serializer = ProjectModelSerializer(instance=page, many=True)
            # 可以使用get_paginated_response 返回数据。源码依然是返回response。进行了结构优化。
            return self.get_paginated_response(serializer.data)
            # 多条数据 要加参数 many=True
        serializer = ProjectModelSerializer(instance=project_qs, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """新增项目"""

        #  1、从前端获取json格式的数据，转换为python当中的类型
        # 为了严谨性，这更需要做各种复杂的检验
        # 比如: 是否为json.传递的项目数据是否符合要求、 有些必传参数是否携带等
        json_data = request.body.decode('utf-8')
        python_data = json.loads(json_data, encoding='utf-8')

        # 反序列化。把数据传给data
        serializer = ProjectModelSerializer(data=python_data)
        # 校验前端输入的数据
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse(serializer.errors,status=400)

        # project = Projects.objects.create(**serializer.validated_data)
        project = serializer.save()

        serializer = ProjectModelSerializer(instance=project)
        return Response(serializer.data,status=201)


class ProjectsDetail(GenericAPIView):
    # # 必须指定queryset 和 serializer_class
    # # queryset 用于指定需要使用的查询集
    queryset = Projects.objects.all()
    # # serializer_class 用于指定需要使用的序列化器
    serializer_class = ProjectModelSerializer
    # def get_object(self,id):
    #     try:
    #         project = Projects.objects.get(id=id)
    #     except Projects.DoesNotExist:
    #         raise Http404
    #     return project

    def get(self, request, pk):

        project = self.get_object()
        # serializer = ProjectSerializer(instance=project,)
        serializer = self.get_serializer(instance=project,)
        return Response(serializer.data)

    def put(self, request, pk):

        # 1、校验前端传递的pk值是否存在。类型是否正确，在数据库中是否存在
        # 2、获取pk值的项目
        project = self.get_object()
        # 从前端获取值
        json_data = request.body.decode('utf-8')
        python_data = json.loads(json_data, encoding='utf-8')

        # 反序列化数据，并校验
        # 将模型类对象转换为字典，并返回
        # 可以同时传参的
        serializer = ProjectSerializer(instance=project, data=python_data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse(serializer.errors)
        # 4、更新项目
        # project.name = serializer.validated_data['name']
        # project.leader = serializer.validated_data['leader']
        # project.tester = serializer.validated_data['tester']
        # project.programer = serializer.validated_data['programer']
        # project.publish_app = serializer.validated_data['publish_app']
        # project.desc = serializer.validated_data['desc']
        #
        # project.save()

        serializer.save()

        return JsonResponse(serializer.data, status=201)

    def delete(self, request, pk):
        # 1、校验前端传递的pk值是否存在。类型是否正确，在数据库中是否存在
        # 2、获取pk值的项目
        project = self.get_object()
        project.delete()
        return JsonResponse(None, safe=False, status=204)











