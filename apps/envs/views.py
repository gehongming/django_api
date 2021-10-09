import json
from django.http import HttpResponse, JsonResponse, Http404


# Create your views here.
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


from envs.models import Envs
from envs.serializer import EnvNameSerializer,EnvsModelSerializer
from rest_framework import viewsets, permissions
from envs.utils import handle_env

class EnvsViewSet(viewsets.ModelViewSet):

    """
    list:
    返回配置(多个)列表数据

    create:
    创建配置

    update:
    更新配置

    partial_update:
    更新(部分)配置

    destroy:
    逻辑删除接口

    names:
    获取所有配置名称和id


    """
    queryset = Envs.objects.filter(is_delete=0)
    serializer_class = EnvsModelSerializer
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


    def list(self, request, *args, **kwargs):
        # 调用父类的list方法。
        response = super().list(request, *args, **kwargs)
        response.data['results'] = handle_env(response.data['results'])
        return response

    def get_serializer_class(self):
        if self.action == 'names':
            return EnvNameSerializer
        else:
            return self.serializer_class



