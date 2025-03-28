"""
URL configuration for MTRPathFinder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from application.views import *
from debug_toolbar.toolbar import debug_toolbar_urls

# 使用 drf_yasg API文档生成器 视图和openapi
from django.views.static import serve
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# 导入权限控制模块
from rest_framework import permissions
schema_view = get_schema_view(
    # API 信息
    openapi.Info(
        title='接口文档',   # API文档标题
        default_version='V1',   # 版本信息
        description='接口文档',    # 描述内容
        # terms_of_service='https://qaq.com',    # 开发团队地址
        # contact=openapi.Contact(email='https://qaq.@qq.com',url='https://qaq.com'),   # 联系人信息：邮件、网址
        license=openapi.License(name='MIT License'),    # 证书
    ),
    public=True,    # 是否公开
    permission_classes=(permissions.AllowAny,)   # 设置用户权限

)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index),
    path('index/', index),
    path('index.html/', index),
    path('index.py/', index),
    path('index.aspx/', index),
    path('index.py/', index),
    path('index.jsp/', index),
    path('index.php/', index),

    path('formtest/', formtest),
    path('stationlist/', stationlist),
    path('image/', image),
    path('error/', error),
    path('include/', include),
    path('release/', release),
    path('issue/', issue),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),   # 互动模式
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),   # 文档模式
]

from django.conf.urls import include
from django.urls import re_path as url

import debug_toolbar
urlpatterns = [
    url('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns