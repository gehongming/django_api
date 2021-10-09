import json
import os
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse, JsonResponse, Http404

# Create your views here.
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from envs.models import Envs
from interfaces.models import Interfaces
from projects.models import Projects
from projects.serializer import ProjectRunSerializer, ProjectModelSerializer, ProjectNameModelSerializer
from rest_framework import viewsets, permissions, status
from projects.utils import get_count_by_project
from testcases.models import TestCases
from utils import common


class ProjectsViewSet(viewsets.ModelViewSet):

    """
    list:
    返回项目(多个)列表数据

    create:
    创建项目

    update:
    更新项目

    partial_update:
    更新(部分)项目

    destroy:
    逻辑删除

    names:
    返回所有项目ID和名称

    interfaces:
    返回某个项目的所有接口信息(ID和名称)
    """
    queryset = Projects.objects.filter(is_delete=0)
    serializer_class = ProjectModelSerializer

    ordering_fields = ['name', 'leader']
    filterset_fields = ['name', 'tester', 'leader', 'id']

    permission_classes = [permissions.IsAuthenticated]
    # 可以使用action装饰器声明自定义的动作
    # 默认情况下，这一个实例方法名就是动作名
    # method,指定动作支持的方法，默认为get
    # detail详情。用于指定该动作处理的是否为详情资源对象(url).url是否需要传递pk值。粗暴理解就是是否传id为True。否则为Fasle

    # 逻辑删除 重写。原有的destroy 是物理删除
    def perform_destroy(self, instance):
        # 修改字段 is_delete
        instance.is_delete = 1
        instance.save()

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # 有分页需求使用。
        # project_qs = self.filter_queryset(queryset)
        # page = self.paginate_queryset(queryset=project_qs)
        # if page:
        #     # 如果配置了分页，page返回不为空。就走这个逻辑
        #     serializer = ProjectNameModelSerializer(instance=page, many=True)
        #     # 可以使用get_paginated_response 返回数据。源码依然是返回response。进行了结构优化。
        #     return self.get_paginated_response(serializer.data)
        # serializer = ProjectNameModelSerializer(instance=project_qs, many=True)

        # 普通的
        # serializer = ProjectNameModelSerializer(instance=queryset, many=True)

        # 使用重写的 get_serializer_class。
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)

    # 获取项目下的接口,因为直接使用序列化器返回的字段。不符合我们的需求，所以就直接写了
    @action(methods=['get'], detail=True)
    def interfaces(self, request, pk=None):
        # instance = self.get_object()
        # serializer = InterfacesByProjectIdSerializer(instance=instance)
        # return Response(serializer.data)

        # if not Projects.objects.only('id').filter(id=pk, is_delete=False):
        #     raise NotFound
        # interface_objs = Interfaces.objects.only('name').filter(project_id=pk, is_delete=False)

        interface_objs = Interfaces.objects.filter(project_id=pk, is_delete=False)
        one_list = []
        for obj in interface_objs:
            one_list.append(
                {'id': obj.id,
                 'name':obj.name})
        return Response(data=one_list)

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        # page = self.paginate_queryset(queryset=queryset)
        #
        # if page:
        #     # 如果配置了分页，page返回不为空。就走这个逻辑
        #     serializer = self.get_serializer(page, many=True)
        #     datas = serializer.data
        #     # 时间格式化，增加统计项目下的数据信息
        #     datas = get_count_by_project(datas)
        #     return self.get_paginated_response(datas)
        #
        # serializer = self.get_serializer(queryset, many=True)
        # datas = serializer.data
        # datas = get_count_by_project(datas)
        # return Response(datas)

        # 调用父类的list方法。
        response = super().list(request, *args, **kwargs)
        response.data['results'] = get_count_by_project(response.data['results'])
        return response

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.validated_data
        env_id = datas.get('env_id')
        # 创建测试用例所在目录名
        testcase_dir_path = os.path.join(settings.SUITES_DIR,
                                         datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
        if not os.path.exists(testcase_dir_path):
            os.mkdir(testcase_dir_path)
        env = Envs.objects.filter(id=env_id, is_delete=0).first()
        # 取出项目下的所有接口
        instance_objs = Interfaces.objects.filter(is_delete=0, project=instance)

        if not instance_objs.exists():
            data_dict = {
                "detail": "此项目下无接口，无法运行！"
            }
            return Response(data_dict, status=status.HTTP_400_BAD_REQUEST)
        # 取出所有接口
        for inter_obj in instance_objs:
            testcase_objs = TestCases.objects.filter(is_delete=0, interface=inter_obj)
            # 取出所有用例
            for one_obj in testcase_objs:
                common.generate_testcase_file(one_obj, env, testcase_dir_path)

        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        """
        重写。根据action的名称 返回使用不同的序列化器。
        :return:
        """
        if self.action == 'names':
            return ProjectNameModelSerializer
        elif self.action == 'run':
            return ProjectRunSerializer
        else:
            return self.serializer_class