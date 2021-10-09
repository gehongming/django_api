from django.db import models
from projects.models import Projects
# Create your models here.
from utils.base_models import BaseModel


class Interfaces(BaseModel):
    id = models.AutoField(verbose_name='id主键', primary_key='True', help_text='id主键')
    name = models.CharField(verbose_name='接口名称', max_length=50, unique=True, help_text='接口名称')
    tester = models.CharField(verbose_name='测试人员', max_length=30, help_text='测试人员')
    desc = models.TextField(verbose_name='简要描述', max_length=200, help_text='简要描述', blank=True, default='默认描述',
                            null=True)
    # 外键放在一对多关系中 多的那一侧。
    # 第一各参数的格式为应用名称.模型类名称。若表在当前应用下，则不需要写应用名称。直接写模型名称，不需要引号
    # 若导入 也可以直接写模型名称
    # 第二个参数设置的是，当父表删除之后，该字段的处理方式
    # project = models.ForeignKey(Projects, on_delete=models.CASCADE,
    #                             verbose_name='所属项目', help_text='所属项目')

    project = models.ForeignKey('projects.Projects', on_delete=models.CASCADE,
                                verbose_name='所属项目', help_text='所属项目')

    # 定义子类meta。用于设置当前数据模型的元数据信息
    class Meta:
        db_table = 'tb_interfaces'
        verbose_name = '接口'
        verbose_name_plural = '接口'

    def __str__(self):
        return self.name