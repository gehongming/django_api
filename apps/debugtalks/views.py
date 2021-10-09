import json
from django.http import HttpResponse, JsonResponse, Http404


# Create your views here.
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework import viewsets, permissions
from rest_framework import filters
from debugtalks.models import DebugTalks
from debugtalks.serializer import DebugTalksSerializer

class DebugTalksViewSet(mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):

    """
    list:
    返回debugtalk(多个)列表数据

    update:
    更新debugtalk

    partial_update:
    更新(部分)debugtalk
    """
    queryset = DebugTalks.objects.filter(is_delete=0)
    serializer_class = DebugTalksSerializer
    ordering_fields = ['id', 'project_id']
    filterset_fields = ['id', 'project_id']
    # 定义权限
    permission_classes = [permissions.IsAuthenticated]

    #获取debugtalk单条详情
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data_dict = {
            "id": instance.id,
            "debugtalk": instance.debugtalk
        }
        return  Response(data_dict)



