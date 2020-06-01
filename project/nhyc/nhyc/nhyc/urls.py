"""nhyc URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from dataProcess import views as dpviews
from django.urls import path, include  ### 현호추가
from django.contrib.auth.models import User  ### 현호추가
from STCService import views as stcViews  ### 현호추가


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/addresses', dpviews.getAddress, name='getAddress'),
    path('admin/houseinfos', dpviews.getHouseInfo, name='getHouseInfo'),
    path('admin/cctvs', dpviews.getCCTV, name='getCCTV'),
    path('admin/securitylights', dpviews.getSecurityLight, name='getSecurityLight'),
    path('admin/policeoffice', dpviews.getPoliceOffice, name='getPoliceOffice'),
  
    ## 현호추가 -->
    path('admin/서울시/', stcViews.getGu),
    path('test/<str:gu>/', stcViews.testQuery),
    path('test/', stcViews.getGu),
    path('houseInfos/', stcViews.houseInfos),
    path('houseInfos/<int:areaCode>/', stcViews.houseInfos),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ## <-- 현호추가
]
