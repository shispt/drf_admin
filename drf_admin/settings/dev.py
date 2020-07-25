"""
Django settings for drf_admin project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import datetime
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mppodn1q7pk7hh)da39+yc1$^rcovyc)$lt69*wprdz_mjayaa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # 解决跨域问题
    'corsheaders',
    # model过滤
    'django_filters',
    # swagger
    'drf_yasg',
    # 注册apps
    'oauth',
    'system',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS跨域设置(3.0版本后需增加http)
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
)
# 允许携带cookie
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'drf_admin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'drf_admin.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 指定自定义的用户模型
AUTH_USER_MODEL = 'oauth.Users'

# DRF配置
REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'drf_admin.utils.exceptions.exception_handler',
    # 全局分页
    'DEFAULT_PAGINATION_CLASS': 'drf_admin.utils.pagination.GlobalPagination',
    'DEFAULT_PERMISSION_CLASSES':
        (
            'drf_admin.utils.permissions.RbacPermission',  # 自定义权限认证
        ),
    "DEFAULT_AUTHENTICATION_CLASSES":
        (
            "rest_framework_jwt.authentication.JSONWebTokenAuthentication",  # DRF-JWT认证
        ),
    # DRF-API文档
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # Token有效时间
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),  # Token刷新有效时间
    'JWT_ALLOW_REFRESH': True,  # 允许刷新Token
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',  # 定义Token携带头信息, Authorization: Bearer ...
}
WHITE_LIST = ['/api/oauth/login/', '/docs/.*']  # 权限认证白名单
REGEX_URL = '^{url}$'  # 严格正则url

DEFAULT_PWD = '123456'  # 创建用户默认密码

AUTHENTICATION_BACKENDS = [
    'oauth.utils.UsernameMobileAuthBackend',  # 自定义用户认证方法
]

# Swagger配置 https://github.com/axnsan12/drf-yasg/issues/58
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

# 日志配置
LOGS_DIR = os.path.join(os.path.dirname(BASE_DIR), 'logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(levelname)s]''[%(filename)s:%(lineno)d][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s]%(message)s'
        },

    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, "info_admin.log"),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 3,
            'formatter': 'simple',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, "err_admin.log"),
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        }

    },
    'loggers': {
        'info': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,
        },
        'warn': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': True,
        },
        'error': {
            'handlers': ['error'],
            'level': 'ERROR',
        }
    }

}
