from django.db import models
from utils.base_models import BaseModel
# Create your models here.


class DebugTalks(BaseModel):
    id = models.AutoField(
        verbose_name='id主键',
        primary_key='True',
        help_text='id主键')
    name = models.CharField(
        verbose_name='debugtalk文件名称',
        max_length=200,
        default='debugtalk.py',
        help_text='debugtalk文件名称')
    debugtalk = models.TextField(
        verbose_name='debugtalk.py文件',
        help_text='debugtalk.py文件',
        default='#debugtalk.py',
        null=True)
    # 一对一关系
    project = models.OneToOneField(
        'projects.Projects',
        on_delete=models.CASCADE,
        verbose_name='所属项目',
        help_text='所属项目',
        related_name='debugtalks')

    class Meta:
        db_table = 'tb_debugtalks'
        verbose_name = 'debugtalk.py文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
