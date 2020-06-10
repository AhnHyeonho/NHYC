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
    path('admin/houseinfos/<int:start>', dpviews.getHouseInfo, name='getHouseInfo'),
    path('admin/houseinfos/<int:start>/<int:end>', dpviews.getHouseInfo, name='getHouseInfo'),
    path('admin/cctvs', dpviews.getCCTV, name='getCCTV'),
    path('admin/securitylights/<str:filename>', dpviews.getSecurityLight, name='getSecurityLight'),
    path('admin/policeoffices', dpviews.getPoliceOffice, name='getPoliceOffice'),
    path('admin/parks', dpviews.getPark, name='getPark'),
    path('admin/markets', dpviews.getMarket, name='getMarket'),
    path('admin/pharmacys', dpviews.getPharmacy, name='getPharmacy'),
    path('admin/culturalfacilities', dpviews.getCulturalFacility, name='getCulturalFacility'),
    path('admin/libraries', dpviews.getLibrary, name='getLibrary'),
    path('admin/concerthalls', dpviews.getConcertHall, name='getConcertHall'),
    path('admin/gyms', dpviews.getGym, name='getGym'),
    path('kakaojoin', stcViews.kakaoJoin, name='kakaoJoin'),
    path('count/<str:id>/<str:category>/<int:milliseconds>', stcViews.count, name='count'),
    path('join', stcViews.join, name='join'),
    path('login', stcViews.login, name='login'),

    # 현호추가 -->

    # 확정 url
    path('admin/initialAddressInfo', stcViews.initialAddressInfo),
    path('admin/updateAvgAddressInfo', stcViews.updateAvgAddressInfo),
    path('getGu/', stcViews.getGu),
    path('getDong/<str:gu>/', stcViews.getDong),
    path('getCCTVCnt/', stcViews.getCCTVCnt),
    path('getCCTVCnt/<str:gu>/', stcViews.getCCTVCnt),
    path('getCCTVCnt/<str:gu>/<str:dong>/', stcViews.getCCTVCnt),
    path('getSecurityLightCnt/', stcViews.getSecurityLightCnt),
    path('getSecurityLightCnt/<str:gu>/', stcViews.getSecurityLightCnt),
    path('getSecurityLightCnt/<str:gu>/<str:dong>/', stcViews.getSecurityLightCnt),
    path('getPoliceOfficeCnt/', stcViews.getPoliceOfficeCnt),
    path('getPoliceOfficeCnt/<str:gu>/', stcViews.getPoliceOfficeCnt),
    path('getPoliceOfficeCnt/<str:gu>/<str:dong>/', stcViews.getPoliceOfficeCnt),

    path('getPharmacyCnt/', stcViews.getPharmacyCnt),
    path('getPharmacyCnt/<str:gu>/', stcViews.getPharmacyCnt),
    path('getPharmacyCnt/<str:gu>/<str:dong>/', stcViews.getPharmacyCnt),
    path('getMarketCnt/', stcViews.getMarketCnt),
    path('getMarketCnt/<str:gu>/', stcViews.getMarketCnt),
    path('getMarketCnt/<str:gu>/<str:dong>/', stcViews.getMarketCnt),
    path('getParkCnt/', stcViews.getParkCnt),
    path('getParkCnt/<str:gu>/', stcViews.getParkCnt),
    path('getParkCnt/<str:gu>/<str:dong>/', stcViews.getParkCnt),
    path('getGymCnt/', stcViews.getGymCnt),
    path('getGymCnt/<str:gu>/', stcViews.getGymCnt),
    path('getGymCnt/<str:gu>/<str:dong>/', stcViews.getGymCnt),
    path('getConcertHallCnt/', stcViews.getConcertHallCnt),
    path('getConcertHallCnt/<str:gu>/', stcViews.getConcertHallCnt),
    path('getConcertHallCnt/<str:gu>/<str:dong>/', stcViews.getConcertHallCnt),
    path('getLibraryCnt/', stcViews.getLibraryCnt),
    path('getLibraryCnt/<str:gu>/', stcViews.getLibraryCnt),
    path('getLibraryCnt/<str:gu>/<str:dong>/', stcViews.getLibraryCnt),
    path('getCulturalFacilityCnt/', stcViews.getCulturalFacilityCnt),
    path('getCulturalFacilityCnt/<str:gu>/', stcViews.getCulturalFacilityCnt),
    path('getCulturalFacilityCnt/<str:gu>/<str:dong>/', stcViews.getCulturalFacilityCnt),

    path('getRankingChartData/<str:division>/', stcViews.getRankingChartData),
    path('getRankingChartData/<str:division>/<str:gu>', stcViews.getRankingChartData),
    path('getTrendChartData/<str:division>/<int:term>/', stcViews.getTrendChartData),
    path('getTrendChartData/<str:division>/<int:term>/<str:gu>', stcViews.getTrendChartData),

    ## 테스트 url
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('test', stcViews.testQuery),
    path('test/<str:division>', stcViews.testQuery),
    path('test/<str:division>/<str:gu>', stcViews.testQuery),
    # path('test/<str:division>/', stcViews.testQuery),
    # path('test/<str:division>/<str:gu>', stcViews.testQuery),

    # dummy data => 추후 삭제
    path('dummyData1/', stcViews.getDummyDataForDH),
    path('dummyData2/', stcViews.getDummyDataForDH2),
    path('dummyData3/', stcViews.getDummyDataForDH3),
    # dummy data => 추후 삭제
    # <-- 현호추가

]
