from django.db import models
from utils.base_models import BaseModel
# Create your models here.


class Reports(BaseModel):
    id = models.AutoField(
        verbose_name='id主键',
        primary_key='True',
        help_text='id主键')
    name = models.CharField(
        verbose_name='报告名称',
        max_length=200,
        unique= True,
        help_text='报告名称')
    result = models.BooleanField(
        "执行结果",
        default=1,  # 1为成功，0为false
        help_text='执行结果',)
    # 一对一关系
    count = models.IntegerField(
        verbose_name='用例总数',
        help_text='用例总数',)
    success = models.IntegerField(
        verbose_name='用例总数',
        help_text='用例总数', )
    html = models.TextField(
        "报告源码",
        help_text="报告源码",
    )
    summary = models.TextField(
        "报告详情",
        help_text="报告详情",
        null=True,
        blank=True,
        default=''
    )

    class Meta:
        db_table = 'tb_reports'
        verbose_name = '测试报告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
