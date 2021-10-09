import json
import os
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse, JsonResponse, Http404


# Create your views here.
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import viewsets, permissions

from envs.models import Envs
from interfaces.models import Interfaces
from utils import common
from utils.handle_datas import handle_data1, handle_data4, handle_data2, handle_data6, handle_data3, handle_data5
from .models import TestCases
from .serializer import TestcasesSerializer, TestcasesRunSerializer


class TestcasesViewSet(viewsets.ModelViewSet):

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
    queryset = TestCases.objects.filter(is_delete=0)
    serializer_class = TestcasesSerializer
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
        # 编辑需要先回显。格式要符合 hrun
        testcase_obj = self.get_object()
        # 用例前置信息
        testcase_include = json.loads(testcase_obj.include)
        # 用例请求信息
        testcase_request = json.loads(testcase_obj.request)
        testcase_request_datas = testcase_request.get('test').get('request')

        # 处理用例的validate列表
        # 将[{'check': 'status_code', 'expected':200, 'comparator': 'equals'}]
        # 转化为 [{key: 'status_code', value: 200, comparator: 'equals', param_type: 'string'}],
        testcase_validate = testcase_request.get('test').get('validate')
        testcase_validate_list = handle_data1(testcase_validate)

        # 处理用例的params数据 request请求模块。
        testcase_parms = testcase_request_datas.get('params')
        testcase_parms_list = handle_data4(testcase_parms)

        # 获取用例的header参数
        testcase_header = testcase_request_datas.get('headers')
        testcase_header_list = handle_data4(testcase_header)

        # 获取variables变量列表
        testcase_variables = testcase_request.get('test').get('variables')
        testcase_variables_list = handle_data2(testcase_variables)

        # 处理form表单数据
        testcase_form_datas = testcase_request_datas.get('data')
        testcase_form_data_list =handle_data6(testcase_form_datas)

        # 处理json数据
        testcase_json_datas = json.dumps(testcase_request_datas.get('json'), ensure_ascii=False)

        #处理extract数据
        testcase_extra_datas = testcase_request.get('test').get('extract')
        testcase_extra_datas_list = handle_data3(testcase_extra_datas)

        # 处理parameters数据
        testcase_parameters_datas = testcase_request.get('test').get('parameters')
        testcase_parameters_datas_list = handle_data3(testcase_parameters_datas)

        # 获取setup_hooks参数
        testcase_setup_hooks_data = testcase_request.get('test').get('setup_hooks')
        testcase_setup_hooks_data = handle_data5(testcase_setup_hooks_data)

        # 获取teardown_hooks参数
        testcase_teardown_hooks_data = testcase_request.get('test').get('teardown_hooks')
        testcase_teardown_hooks_data = handle_data5(testcase_teardown_hooks_data)

        selected_configure_id = testcase_include.get('config')
        selected_interface_id = testcase_obj.interface_id
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project_id
        selected_testcase_id = testcase_include.get('testcases')
        # 构造数据
        data = {
            "author": testcase_obj.author,
            "testcase_name": testcase_obj.name,
            "selected_configure_id": selected_configure_id,
            "selected_interface_id": testcase_obj.interface_id,
            "selected_project_id": selected_project_id,
            "selected_testcase_id": selected_testcase_id,

            "method": testcase_request_datas.get('method'),
            "url": testcase_request_datas.get('url'),
            "param": testcase_parms_list,
            "header": testcase_header_list,
            "variable": testcase_form_data_list,
            "jsonVariable": testcase_json_datas,

            "extract": testcase_extra_datas_list,
            "validate": testcase_validate_list,
            # 用例的当前配置（variables）
            "globalVar": testcase_variables_list,
            "parameterized": testcase_parameters_datas_list,
            "setupHooks": testcase_setup_hooks_data,
            "teardownHooks": testcase_teardown_hooks_data
        }

        return Response(data)

    @action(methods=['post'], detail=True)
    def run(self,request, *args, **kwargs):
        # 1、取出用例模型对象并获取env_id
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        # 校验数据是否正确
        serializer.is_valid(raise_exception=True)
        datas = serializer.validated_data

        env_id = datas.get('env_id')

        # 2、创建以时间戳命名的目录
        dirname = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        testcase_dir_path = os.path.join(settings.SUITES_DIR, dirname)
        os.makedirs(testcase_dir_path)
        # 获取环境变量
        env = Envs.objects.filter(id=env_id, is_delete=0).first()

        # 3、创建以项目名命名的目录
        # 4、生成debugtalks.py、yaml用例文件
        common.generate_testcase_file(instance, env, testcase_dir_path)

        # 5、运行用例并生成测试报告
        return common.run_testcase(instance, testcase_dir_path)
        # qs = [self.get_object()]
        # return self.execute(qs)

    def get_serializer_class(self):
        return TestcasesRunSerializer if self.action == 'run' else self.serializer_class

