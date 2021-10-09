import json
import re
import os
from datetime import datetime

from django.http import StreamingHttpResponse
from django.utils.encoding import escape_uri_path
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.settings import settings

from .models import Reports
from .serializer import ReportsSerializer
from .utils import format_output, get_file_contents


class ReportsViewSet(ModelViewSet):

    """
    list:
    返回测试报告(多个)列表数据

    create:
    创建测试报告

    update:
    更新测试报告

    partial_update:
    更新(部分)测试报告

    destroy:
    逻辑删除测试报告

    retrieve:
    获取测试报告详情
    """
    queryset = Reports.objects.filter(is_delete=0)
    serializer_class = ReportsSerializer

    ordering_fields = ['name']
    # 定义权限
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # 调用父类的list方法。
        response = super().list(request, *args, **kwargs)
        response.data['results'] = format_output(response.data['results'])
        return response

    # 逻辑删除 重写。原有的destroy 是物理删除
    def perform_destroy(self, instance):
        # 修改字段 is_delete
        instance.is_delete = 1
        instance.save()

    @action(detail=True)
    def download(self, request, pk=None):

        # 1、获取html源码
        instance = self.get_object()
        html = instance.html
        name = instance.name

        # 正则取存储的文件名称
        mtch = re.match(r'(.*_)\d+', name)
        if mtch:
            mtch = mtch.group(1)
            report_filename = mtch + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S' + '.html')
        # 获取文件路径。可以通过settings.BASE_DI获取项目路径
        else:
            report_filename = name+'.html'
        # settings.REPORTS_DIR 设置 报告目录。
        report_path = os.path.join(settings.REPORTS_DIR, report_filename)

        # 将html数据 写入到保存的html文件内。
        with open(report_path, 'w+', encoding='utf-8') as one_file:
            one_file.write(html)

        # 下载专用返回格式
        response = StreamingHttpResponse(get_file_contents(report_path))
        report_path_final = escape_uri_path(report_filename)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f"attachment; filename*=UTF-8''{report_path_final}"
        return response

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        try:
            data['summary'] = json.loads(data['summary'], encoding='utf-8')
            return Response(data)
        except Exception as e:
            return Response({
                        'err': '测试报告summary格式有误'
                    }, status=status.HTTP_400_BAD_REQUEST)


    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     try:
    #         summary = json.loads(instance.summary, encoding='utf-8')
    #         return Response({
    #             'id': instance.id,
    #             'summary': summary
    #         }, status=status.HTTP_200_OK)
    #     except Exception:
    #         return Response({
    #             'err': '测试报告summary格式有误'
    #         }, status=status.HTTP_400_BAD_REQUEST)




