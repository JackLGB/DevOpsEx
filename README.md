# devopsex
 DevOps System

## 1、安装开源库
### 1.1 安装django版本==4.1，这是python web框架
```shell
pip install django==4.1
```
### 1.2 安装channels，这是websocket支持包
```shell
pip install channels
```
说明文档:https://channels.readthedocs.io/en/latest/introduction.html

### 1.3 安装rest_framework，这是序列化器

```shell
pip install djangorestframework
```

## 2、配置web程序
### 2.1 配置settings.py文件

#### 2.1.1 配置ALLOWED_HOSTS

```python
ALLOWED_HOSTS = ["*"]  # "*"表示所有地址可访问
```

#### 2.1.2 配置channels、rest_framework

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ![1] 在这个位置添加app名称，激活app
    "channels",  # 通道
    "rest_framework",  # 序列化器
]
```

#### 2.1.3 配置数据库

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # ![2]数据库配置
}
```
MariaDB、MySQL、Oracle 或 PostgreSQL数据库需要额外的连接参数，例如：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
其中ENGINE可以设置为：
```python
'django.db.backends.postgresql'
'django.db.backends.mysql'
'django.db.backends.sqlite3'
'django.db.backends.oracle'
```

#### 2.1.4 配置asgi

```python
ASGI_APPLICATION = 'DevOpsEx.asgi.application'
```
#### 2.1.5 配置日志
- 如果不想配置日志记录器，则
```python
LOGGING_CONFIG = None
```
- 如果需要设置日志记录器，则
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file-DEBUG': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'MIDNIGHT',  # 旋转日志（切换新的日志文件）的方式
            'interval': 1,  # 旋转的时间间隔
            'formatter': 'simple',  # 输出处理器
            'backupCount': 30 * 6,  # 备份天数,单位天
            'filename': './log/debug.log',
        },
        'file-ERROR': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'MIDNIGHT',  # 旋转日志（切换新的日志文件）的方式
            'interval': 1,  # 旋转的时间间隔
            'formatter': 'verbose',  # 输出处理器
            'backupCount': 30 * 6,  # 备份天数,单位天
            'filename': './log/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file-DEBUG', 'file-ERROR'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file-ERROR'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
```



### 2.2 配置asgi.py文件

```python
import os

from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DevOpsEx.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': URLRouter([
        # 书写websocket路由与视图函数对应关系
    ])
})

```
## 2.3 配置DevOpsEx/DevOpsEx/urls.py
```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include('rest_framework.urls')),# 添加framework的配置
]
```


