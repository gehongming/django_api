import json
from django.http import HttpResponse, JsonResponse, Http404


# Create your views here.
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from configures.models import Configures
from interfaces.models import Interfaces
from interfaces.serializer import InterfaceModelSerializer, InterfaceNameModelSerializer

from rest_framework import viewsets, permissions

from interfaces.utils import get_count_by_interface
from testcases.models import TestCases


class InterfacesViewSet(viewsets.ModelViewSet):

    """
    list:
    返回接口(多个)列表数据

    create:
    创建接口

    update:
    更新接口

    partial_update:
    更新(部分)接口

    destroy:
    逻辑删除接口

    retrieve:
    获取接口详情

    names:
    获取所有接口名称和id

    configures：
    获取接口下 配置名称和id

    testcases：
    获取接口下 测试用例名称和id
    """
    queryset = Interfaces.objects.filter(is_delete=0)
    serializer_class = InterfaceModelSerializer

    ordering_fields = ['name']
    filterset_fields = ['name', 'id']
    # 定义权限
    permission_classes = [permissions.IsAuthenticated]

    # 逻辑删除 重写。原有的destroy 是物理删除
    def perform_destroy(self, instance):
        # 修改字段 is_delete
        instance.is_delete = 1
        instance.save()

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def configs(self, request, pk=None):

        configures_objs = Configures.objects.filter(interface_id=pk, is_delete=False)
        one_list = []
        for obj in configures_objs:
            one_list.append(
                {'id': obj.id,
                 'name':obj.name})
        return Response(data=one_list)

    @action(methods=['get'], detail=True)
    def testcases(self, request, pk=None):

        testcases_objs = TestCases.objects.filter(interface_id=pk, is_delete=False)
        one_list = []
        for obj in testcases_objs:
            one_list.append(
                {'id': obj.id,
                 'name': obj.name})
        return Response(data=one_list)

    def list(self, request, *args, **kwargs):
        # 调用父类的list方法。
        response = super().list(request, *args, **kwargs)
        response.data['results'] = get_count_by_interface(response.data['results'])
        return response

    def get_serializer_class(self):
        if self.action == 'names':
            return InterfaceNameModelSerializer
        else:
            return self.serializer_class



