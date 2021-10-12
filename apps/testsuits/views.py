import json
import os.path
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse, JsonResponse, Http404


# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response

from envs.models import Envs
from testcases.models import TestCases
from utils import common
from .models import Testsuits
from rest_framework import viewsets, permissions, status
from .serializer import TestsuitsModelSerializer, TestsuitsRunSerializer
from .utils import get_testcases_by_interfaces_id


class TestsuitsViewSet(viewsets.ModelViewSet):

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
    queryset = Testsuits.objects.filter(is_delete=0)
    serializer_class = TestsuitsModelSerializer

    ordering_fields = ['name', 'id']

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

    def retrieve(self, request, *args, **kwargs):
        """
        获取用例详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        testsuit_obj = self.get_object()

        datas = {
            "name": testsuit_obj.name,
            "project_id": testsuit_obj.project_id,
            "include": testsuit_obj.include
        }
        return Response(datas)

    @action(methods=['POST'],detail=True)
    def run(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.validates_data
        env_id = datas.get('env_id')

        # 创建测试用例所在目录名
        testcase_dir_path = os.path.join(settings.SUITES_DIR,
                                         datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))

        if not os.path.exists(testcase_dir_path):
            os.mkdir(testcase_dir_path)

        env = Envs.objects.filter(id=env_id, is_delete=0).first()
        include = eval(instance.include)
        if len(include) == 0:
            data_dict = {
                "detail": "此套件下无接口，无法运行！"
            }
            return Response(data_dict, status=status.HTTP_400_BAD_REQUEST)
        # 取出所有接口
        include = get_testcases_by_interfaces_id(include)
        for testcase_id in include:
            testcase_obj = TestCases.objects.filter(is_delete=0, interface=testcase_id)
            # 取出所有用例
            if testcase_obj:
                common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == 'run' :
            return TestsuitsRunSerializer
        else:
            return self.serializer_class