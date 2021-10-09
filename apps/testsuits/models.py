from django.db import models

from projects.models import Projects
from utils.base_models import BaseModel
# Create your models here.


class Testsuits(BaseModel):
    id = models.AutoField(
        verbose_name='id主键',
        primary_key='True',
        help_text='id主键')
    name = models.CharField(
        verbose_name='套件名称',
        max_length=200,
        help_text='配置名称')
    project = models.ForeignKey('projects.Projects', on_delete=models.CASCADE,
                                verbose_name='所属接口', help_text='所属接口',
                                related_name='testsuits')
    include = models.TextField(
        verbose_name='包含的接口',
        help_text='包含的接口',
        null=False)

    class Meta:
        db_table = 'tb_testsuits'
        verbose_name = '套件信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
