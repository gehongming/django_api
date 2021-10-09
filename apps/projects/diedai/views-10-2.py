import json
from django.http import HttpResponse, JsonResponse, Http404


# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response

from projects.models import Projects
from projects.serializer import InterfaceNameSerializer, InterfacesByProjectIdSerializer, ProjectModelSerializer, ProjectNameModelSerializer

from rest_framework import viewsets, permissions


class ProjectsViewSet(viewsets.ModelViewSet):

    """
    create:
    创建项目

    update:
    更新项目

    list:
    获取所有项目
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer

    ordering_fields = ['name', 'leader']
    filterset_fields = ['name', 'tester', 'leader', 'id']

    permission_classes = [permissions.IsAuthenticated]
    # 可以使用action装饰器声明自定义的动作
    # 默认情况下，这一个实例方法名就是动作名
    # method,指定动作支持的方法，默认为get
    # detail详情。用于指定该动作处理的是否为详情资源对象(url).url是否需要传递pk值。粗暴理解就是是否传id为True。否则为Fasle

    @action(methods=['get'], detail=False, url_path='nm', url_name='url_name')
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        project_qs = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset=project_qs)
        if page:
            # 如果配置了分页，page返回不为空。就走这个逻辑
            serializer = ProjectNameModelSerializer(instance=page, many=True)
            # 可以使用get_paginated_response 返回数据。源码依然是返回response。进行了结构优化。
            return self.get_paginated_response(serializer.data)
        serializer = ProjectNameModelSerializer(instance=project_qs, many=True)
        return Response(serializer.data)

    # 获取项目下的接口
    @action(methods=['get'], detail=True)
    def interfaces(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = InterfacesByProjectIdSerializer(instance=instance)
        return Response(serializer.data)



