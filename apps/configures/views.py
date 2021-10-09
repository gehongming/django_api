import json

from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.handle_datas import handle_data4, handle_data2
from .models import Configures
from .serializer import ConfiguresSerializer
from interfaces.models import Interfaces
from utils import handle_datas
# Create your views here.


class ConfiguresViewSet(ModelViewSet):
    """
        list:
        返回接口(多个)配置数据

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
    queryset = Configures.objects.filter(is_delete=0)
    serializer_class = ConfiguresSerializer

    ordering_fields = ['name']
    # 定义权限
    permission_classes = [permissions.IsAuthenticated]

    # 逻辑删除 重写。原有的destroy 是物理删除
    def perform_destroy(self, instance):
        # 修改字段 is_delete
        instance.is_delete = 1
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        # 编辑需要先回显。格式要符合 hrun
        config_obj = self.get_object()
        config_request = json.loads(config_obj.request, encoding='utf-8')
        # 处理请求头数据：格式是因为前端需要改格式。嵌套字典的列表。
        config_header = config_request['config']['request'].get('headers')
        config_header_list = handle_data4(config_header)

        # 处理全局变量数据
        config_variables=config_request['config'].get('variables')
        config_variables_list = handle_data2(config_variables )

        # 配置名称name
        config_name=config_request['config']['name']

        # 接口id、项目id
        selected_interface_id = config_obj.interface_id
        selected_project_id = Interfaces.objects.get(id = selected_interface_id).project_id

        # 构造数据
        data = {
            'author': config_obj.author,
            'configure_name': config_name,
            'selected_project_id': selected_project_id,
            'selected_interface_id': selected_interface_id,
            'header': config_header_list,
            'globalVar': config_variables_list
        }

        return Response(data)

    # def get_serializer_class(self):
    #     if self.action == 'names':
    #         return InterfaceNameModelSerializer
    #     else:
    #         return self.serializer_class


