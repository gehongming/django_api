from django.contrib import admin
from .models import Projects, Person
# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    # 指定在修改（新增）中需要显示的字段
    fields = ('name', 'leader','tester')
    # 指定要列出的字段
    list_display = ['name', 'leader','tester']


admin.site.register(Projects, ProjectAdmin)
admin.site.register(Person)
