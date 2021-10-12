"""
Django settings for django_api project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import sys
import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# SYS.PATH 是一个列表。所以我们可以插入一条路径。
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 测试报告HTML文件所在目录
REPORTS_DIR = os.path.join(BASE_DIR, 'report')
# 测试yaml文件 所在目录
SUITES_DIR = os.path.join(BASE_DIR, 'suite')
PROJECT_DIR = os.path.join(BASE_DIR, 'projects_dir')

# 指定用于收集静态文件服务的路径.打包专用
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@grn2g$9o0@yw3)l#&&el6*s&a*oo(g*nqb@&n(qnv%+32+xox'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    # 第三方
    'rest_framework',
    'django_filters',
    'drf_yasg',
    # 自己的应用
    'projects.apps.ProjectsConfig',
    'interfaces.apps.InterfacesConfig',
    'user.apps.UserConfig',
    'configures.apps.ConfiguresConfig',
    'testcases.apps.TestcasesConfig',
    'testsuits.apps.TestsuitsConfig',
    'reports.apps.ReportsConfig',
    'envs.apps.EnvsConfig',
    'debugtalks.apps.DebugtalksConfig',
    'summary.apps.SummaryConfig',
    # 'index.apps.IndexConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_api.urls'

CORS_ORIGIN_ALLOW_ALL = True
# 允许跨域时携带Cookie,默认为 False
CORS_ALLOW_CREDENTIALS = True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_api.wsgi.application'

REST_FRAMEWORK = {
    # 默认响应渲染类
    'DEFAULT_ RENDERER_ CLASSES': (
        # json渲染器为第一优先级
        'rest_framework.renderers.JSONRenderer'
        # 可浏览的API渲染器为第二优先级。浏览器打开为可操作页面。
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': ['rest_framework.filters.OrderingFilter',
                               'django_filters.rest_framework.backends.DjangoFilterBackend'],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 5,
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.PageNumberPaginationManual',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',

    # 'DEFAULT_PERMISSION_CLASSES': [
    # 'rest_framework.permissions.IsAuthenticated',
    # ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 指定使用 Token认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # session会话认证
        'rest_framework.authentication.SessionAuthentication',
        # Basic类型的认证（账号和密码）
        'rest_framework.authentication.BasicAuthentication'
    ],
}
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

JWT_AUTH = {
    # 默认有效时间为：5min，改为1天。
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # TOken 前缀
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'utils.jwt_handler.jwt_response_payload_handler',

}

DATABASES = {
    # 实际操作不会用
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        # 指定引擎
        'ENGINE': 'django.db.backends.mysql',
        # 指定数据库名称
        'NAME': 'my_django2',
        # 数据库用户名，root账号默认不能远程登录
        'USER': 'ghm',
        'PASSWORD': '123456',
        'HOST': '121.43.178.79',
        'PORT': 3306
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path): os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个

LOGGING = {
    # 版本
    'version': 1,
    # 是否禁用已存在的日志器
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs/mytest.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

