"""django_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path
from django.urls import include
# from demo1.views import index
from django.views import static
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.static import serve

schema_view = get_schema_view(
    openapi.Info(
        title='接口文档',  #必传，
        default_version='v1' , #必传
        description='这是优秀的接口文档',
        terms_of_service='http:api.niuniu.com',
        contact=openapi.Contact(email='1010562639@qq.com'),
        license=openapi.License(name='BSD LICENSE'),
    ),
    public=True,
)

urlpatterns = [
    # 站点管理
    path('admin/', admin.site.urls),
    # docs 接口文档
    path('docs/', include_docs_urls(title='测试平台接口文档')),

    # swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # 自己的的应用
    # include:去子应用的urls文件去查找
    path('', include('projects.urls')),
    path('', include('testcases.urls')),
    path('', include('interfaces.urls')),
    path('', include('envs.urls')),
    path('', include('debugtalks.urls')),
    path('', include('testsuits.urls')),
    path('', include('configures.urls')),
    path('', include('summary.urls')),
    path('', include('reports.urls')),
    path('api/', include('rest_framework.urls')),
    path('user/', include('user.urls')),
    # 静态文件,前后端代码合并使用.
]