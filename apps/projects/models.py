from django.db import models
from utils.base_models import BaseModel
# Create your models here.


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        # 表名-字符串名称小写
        # 格式为tb_数据库名称
        db_table = 'tb_Person'
        # 会在admin站点中，显示一个更人性化的表名
        verbose_name = '人员'
        # verbose_name的复数形式。名称直接和verbose_name一致即可。会自动加s
        verbose_name_plural = '人员'

    def __str__(self):
        return self.first_name


class Projects(BaseModel):
    # 目的就是设置成中文。当字段存在 primary_key='True'属性，就不会给我们自动新建主键了
    id = models.AutoField(verbose_name='id主键', primary_key='True', help_text='id主键')
    name = models.CharField(verbose_name='项目名称', max_length=50, unique=True, help_text='项目名称')
    leader = models.CharField(verbose_name='负责人', max_length=30,  help_text='负责人')
    tester = models.CharField(verbose_name='测试人员', max_length=30,  help_text='测试人员')
    programmer = models.CharField(verbose_name='开发人员', max_length=30, help_text='开发人员')
    publish_app = models.CharField(verbose_name='发布应用', max_length=100, help_text='发布应用')
    desc = models.TextField(verbose_name='简要描述', max_length=200, help_text='简要描述', blank=True, default='默认描述', null=True)

    # 定义子类meta。用于设置当前数据模型的元数据信息
    class Meta:
        # 表名-字符串名称小写
        # 格式为tb_数据库名称
        db_table = 'tb_projects'
        # 会在admin站点中，显示一个更人性化的表名
        verbose_name = '项目'
        # verbose_name的复数形式。名称直接和verbose_name一致即可。会自动加s
        verbose_name_plural = '项目'

    def __str__(self):
        return self.name

