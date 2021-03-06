"""CMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.views.generic.base import TemplateView

from crm.views import account,home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', account.login),
    path('index/', account.index,name="index"),
    path('logout/', account.logout),
    path('upload.html', account.upload),
    path('del_img.html', account.del_img),
    path(r'',TemplateView.as_view(template_name='index.html')),
    # 路由分发
    path(r'crm/',include(('crm.urls','crm'),namespace='crm')),
    #path(r'register/',views.register),
    path(r'redis_index/', account.redis_index),
]
