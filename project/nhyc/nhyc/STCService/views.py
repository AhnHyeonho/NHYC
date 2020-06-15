import inspect
import os
from sklearn.preprocessing import MinMaxScaler
from collections import OrderedDict
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet, RawQuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Value, FloatField, F
from knox.models import AuthToken
import knox.auth
from rest_framework.authtoken.serializers import AuthTokenSerializer
import json, xmltodict
import xml.etree.ElementTree as ET
import pandas
import numpy as np
import httplib2

from dataProcess.models import Member
from .serializers import MemberSerializer
from dataProcess.models import MemberInfo
from .serializers import MemberInfoSerializer
from dataProcess.models import HouseInfo
from .serializers import HouseInfoSerializer
from dataProcess.models import CCTV
from .serializers import CCTVSerializer
from dataProcess.models import PoliceOffice
from .serializers import PoliceOfficeSerializer
from dataProcess.models import SecurityLight
from .serializers import SecurityLightSerializer
from dataProcess.models import Address
from .serializers import AddressSerializer
from dataProcess.models import CostRecord
from .serializers import CostRecordSerializer
from dataProcess.models import AddressInfo
from dataProcess.models import FrequentPlace
from .models import Average, Result_GuCnt, Result_GuDongCnt, TrendChartData, BubbleChartData
from dataProcess.models import MemberTrend
from dataProcess.models import TrendBySession
from dataProcess.models import RecommendedDong
from dataProcess.models import Recommendation
from dataProcess.models import AddressInfo
from dataProcess.models import FrequentPlace

import nhyc.settings as settings

# 서울시 행정구
seoulGu = {'중구': '10100',
           '종로구': '10110',
           '서대문구': '10120',
           '마포구': '10121',
           '은평구': '10122',
           '동대문구': '10130',
           '중랑구': '10131',
           '도봉구': '10132',
           '성동구': '10133',
           '강동구': '10134',
           '강남구': '10135',
           '성북구': '10136',
           '서초구': '10137',
           '송파구': '10138',
           '노원구': '10139',
           '용산구': '10140',
           '강북구': '10142',
           '광진구': '10143',
           '영등포구': '10150',
           '관악구': '10151',
           '구로구': '10152',
           '금천구': '10153',
           '동작구': '10156',
           '강서구': '10157',
           '양천구': '10158'}


########################## ↓↓↓↓↓↓↓↓ ############################
@csrf_exempt
def myJsonResponse(data):
    return HttpResponse(json.dumps(data, ensure_ascii=False))


@csrf_exempt
def getGu(request):
    # 구 이름만 배열로..
    returnString = []
    for i in seoulGu:
        returnString.append(i)
        print(i)
    returnString.sort()  # 구 내용 정렬
    return myJsonResponse(returnString)


@csrf_exempt
def getDong(request, gu):
    # 구이름 입력하면 동 리스트 리턴
    resultString = []
    querySet = Address.objects.filter(gu=gu).order_by('dong')
    for i in querySet:
        resultString.append(i.dong)
        print(i.dong)
    return myJsonResponse(resultString)


@csrf_exempt
def getCCTVCnt(request, gu=None, dong=None):
    '''
    :param request: 
    :param gu: 
    :return: 서울시 내의 구들의 cctv 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 cctv 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 cctv 갯수를 리턴 (값 1개)
    '''
    resultList = []
    if gu is None:
        print('시 cctv 데이터 출력')
        querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totCCTV')).values('gu', 'totalCnt').order_by(
            'gu')
    else:
        if dong is None:
            print('{} cctv 데이터 출력'.format(gu))
            querySet = AddressInfo.objects.filter(gu=gu).values('dong').annotate(totalCnt=Sum('totCCTV')).order_by(
                'dong')
        else:
            print('{} {} cctv 데이터 출력'.format(gu, dong))
            querySet = AddressInfo.objects.filter(gu=gu, dong=dong).values('dong').annotate(
                totalCnt=Sum('totCCTV')).order_by('dong')

    for i in querySet:
        resultList.append(i['totalCnt'])
        print(i['totalCnt'])

    return myJsonResponse(resultList)


@csrf_exempt
def getSecurityLightCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 보안등 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 보안등 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 보안등 갯수를 리턴 (값 1개)
    '''
    resultList = []
    if gu is None:
        print('시 보안등 데이터 출력')
        querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totLight')).values('gu',
                                                                                              'totalCnt').order_by(
            'gu')
    else:
        if dong is None:
            print('{} 보안등 데이터 출력'.format(gu))
            querySet = AddressInfo.objects.filter(gu=gu).values('dong').annotate(totalCnt=Sum('totLight')).order_by(
                'dong')
        else:
            print('{} {} 보안등 데이터 출력'.format(gu, dong))
            querySet = AddressInfo.objects.filter(gu=gu, dong=dong).values('dong').annotate(
                totalCnt=Sum('totLight')).order_by('dong')
    for i in querySet:
        resultList.append(i['totalCnt'])
        print(i['totalCnt'])

    return myJsonResponse(resultList)


@csrf_exempt
def getPoliceOfficeCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 경찰시설 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 경찰시설 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 경찰시설 갯수를 리턴 (값 1개)
    '''
    resultList = []
    if gu is None:
        print('시 경찰시설 데이터 출력')
        querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totPolice')).values('gu',
                                                                                               'totalCnt').order_by(
            'gu')
    else:
        if dong is None:
            print('{} 경찰시설 데이터 출력'.format(gu))
            querySet = AddressInfo.objects.filter(gu=gu).values('dong').annotate(totalCnt=Sum('totPolice')).order_by(
                'dong')
        else:
            print('{} {} 경찰시설 데이터 출력'.format(gu, dong))
            querySet = AddressInfo.objects.filter(gu=gu, dong=dong).values('dong').annotate(
                totalCnt=Sum('totPolice')).order_by('dong')
    for i in querySet:
        resultList.append(i['totalCnt'])
        print(i['totalCnt'])

    return myJsonResponse(resultList)


@csrf_exempt
def getPharmacyCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 약국 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 약국 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 약국 갯수를 리턴 (값 1개)
    '''
    resultList = []
    if gu is None:
        print('시 약국 데이터 출력')
        querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totPharmacy')).values('gu',
                                                                                                 'totalCnt').order_by(
            'gu')
    else:
        if dong is None:
            print('{} 약국 데이터 출력'.format(gu))
            querySet = AddressInfo.objects.filter(gu=gu).values('dong').annotate(totalCnt=Sum('totPharmacy')).order_by(
                'dong')
        else:
            print('{} {} 약국 데이터 출력'.format(gu, dong))
            querySet = AddressInfo.objects.filter(gu=gu, dong=dong).values('dong').annotate(
                totalCnt=Sum('totPharmacy')).order_by('dong')
    for i in querySet:
        resultList.append(i['totalCnt'])
        print(i['totalCnt'])

    return myJsonResponse(resultList)


@csrf_exempt
def getMarketCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 전통시장 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 전통시장 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 전통시장 갯수를 리턴 (값 1개)
    '''
    resultList = []
    if gu is None:
        print('시 전통시장 데이터 출력')
        querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totMarket')).values('gu',
                                                                                               'totalCnt').order_by(
            'gu')
    else:
        if dong is None:
            print('{} 전통시장 데이터 출력'.format(gu))
            querySet = AddressInfo.objects.filter(gu=gu).values('dong').annotate(totalCnt=Sum('totMarket')).order_by(
                'dong')
        else:
            print('{} {} 전통시장 데이터 출력'.format(gu, dong))
            querySet = AddressInfo.objects.filter(gu=gu, dong=dong).values('dong').annotate(
                totalCnt=Sum('totMarket')).order_by('dong')
    for i in querySet:
        resultList.append(i['totalCnt'])
        print(i['totalCnt'])

    return myJsonResponse(resultList)


@csrf_exempt
def getParkCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 공원 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 공원 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 공원 갯수를 리턴 (값 1개)
    '''
    resultList = []
    if gu is None:
        print('시 공원 데이터 출력')
        querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totPark')).values('gu',
                                                                                             'totalCnt').order_by(
            'gu')
    else:
        if dong is None:
            print('{} 공원 데이터 출력'.format(gu))
            querySet = AddressInfo.objects.filter(gu=gu).values('dong').annotate(totalCnt=Sum('totPark')).order_by(
                'dong')
        else:
            print('{} {} 공원 데이터 출력'.format(gu, dong))
            querySet = AddressInfo.objects.filter(gu=gu, dong=dong).values('dong').annotate(
                totalCnt=Sum('totPark')).order_by('dong')
    for i in querySet:
        resultList.append(i['totalCnt'])
        print(i['totalCnt'])

    return myJsonResponse(resultList)


@csrf_exempt
def getGymCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 공공체육시설 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 공공체육시설 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 공공체육시설 갯수를 리턴 (값 1개)
    '''
    resultList = []
    if gu is None:
        print('시 공공체육시설 데이터 출력')
        querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totGym')).values('gu',
                                                                                            'totalCnt').order_by(
            'gu')
    else:
        if dong is None:
            print('{} 공공체육시설 데이터 출력'.format(gu))
            querySet = AddressInfo.objects.filter(gu=gu).values('dong').annotate(totalCnt=Sum('totGym')).order_by(
                'dong')
        else:
            print('{} {} 공공체육시설 데이터 출력'.format(gu, dong))
            querySet = AddressInfo.objects.filter(gu=gu, dong=dong).values('dong').annotate(
                totalCnt=Sum('totGym')).order_by('dong')
    for i in querySet:
        resultList.append(i['totalCnt'])
        print(i['totalCnt'])

    return myJsonResponse(resultList)


@csrf_exempt
def getConcertHallCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 공연장 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 공연장 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 공연장 갯수를 리턴 (값 1개)
    '''
    resultList = []
    if gu is None:
        print('시 공연장 데이터 출력')
        querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totConcertHall')).values('gu',
                                                                                                    'totalCnt').order_by(
            'gu')
    else:
        if dong is None:
            print('{} 공연장 데이터 출력'.format(gu))
            querySet = AddressInfo.objects.filter(gu=gu).values('dong').annotate(
                totalCnt=Sum('totConcertHall')).order_by(
                'dong')
        else:
            print('{} {} 공연장 데이터 출력'.format(gu, dong))
            querySet = AddressInfo.objects.filter(gu=gu, dong=dong).values('dong').annotate(
                totalCnt=Sum('totConcertHall')).order_by('dong')
    for i in querySet:
        resultList.append(i['totalCnt'])
        print(i['totalCnt'])

    return myJsonResponse(resultList)


@csrf_exempt
def getLibraryCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 도서관 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 도서관 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 도서관 갯수를 리턴 (값 1개)
    '''
    resultList = []
    if gu is None:
        print('시 도서관 데이터 출력')
        querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totLibrary')).values('gu',
                                                                                                'totalCnt').order_by(
            'gu')
    else:
        if dong is None:
            print('{} 도서관 데이터 출력'.format(gu))
            querySet = AddressInfo.objects.filter(gu=gu).values('dong').annotate(totalCnt=Sum('totLibrary')).order_by(
                'dong')
        else:
            print('{} {} 도서관 데이터 출력'.format(gu, dong))
            querySet = AddressInfo.objects.filter(gu=gu, dong=dong).values('dong').annotate(
                totalCnt=Sum('totLibrary')).order_by('dong')
    for i in querySet:
        resultList.append(i['totalCnt'])
        print(i['totalCnt'])

    return myJsonResponse(resultList)


@csrf_exempt
def getSubwayCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 지하철역 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 지하철역 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 지하철역 갯수를 리턴 (값 1개)
    '''
    resultList = []
    if gu is None:
        print('시 지하철역 데이터 출력')
        querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totSubway')).values('gu',
                                                                                               'totalCnt').order_by(
            'gu')
    else:
        if dong is None:
            print('{} 지하철역 데이터 출력'.format(gu))
            querySet = AddressInfo.objects.filter(gu=gu).values('dong').annotate(totalCnt=Sum('totSubway')).order_by(
                'dong')
        else:
            print('{} {} 지하철역 데이터 출력'.format(gu, dong))
            querySet = AddressInfo.objects.filter(gu=gu, dong=dong).values('dong').annotate(
                totalCnt=Sum('totSubway')).order_by('dong')
    for i in querySet:
        resultList.append(i['totalCnt'])
        print(i['totalCnt'])

    return myJsonResponse(resultList)


@csrf_exempt
def getBusCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 버스정류장 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 버스정류장 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 버스정류장 갯수를 리턴 (값 1개)
    '''
    resultList = []
    if gu is None:
        print('시 버스정류장 데이터 출력')
        querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totBus')).values('gu',
                                                                                            'totalCnt').order_by(
            'gu')
    else:
        if dong is None:
            print('{} 버스정류장 데이터 출력'.format(gu))
            querySet = AddressInfo.objects.filter(gu=gu).values('dong').annotate(totalCnt=Sum('totBus')).order_by(
                'dong')
        else:
            print('{} {} 버스정류장 데이터 출력'.format(gu, dong))
            querySet = AddressInfo.objects.filter(gu=gu, dong=dong).values('dong').annotate(
                totalCnt=Sum('totBus')).order_by('dong')
    for i in querySet:
        resultList.append(i['totalCnt'])
        print(i['totalCnt'])

    return myJsonResponse(resultList)


@csrf_exempt
def getCulturalFacilityCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 박물관/미술관 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 박물관/미술관 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 박물관/미술관 갯수를 리턴 (값 1개)
    '''
    resultList = []
    if gu is None:
        print('시 박물관/미술관 데이터 출력')
        querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totCulturalFacility')).values('gu',
                                                                                                         'totalCnt').order_by(
            'gu')
    else:
        if dong is None:
            print('{} 박물관/미술관 데이터 출력'.format(gu))
            querySet = AddressInfo.objects.filter(gu=gu).values('dong').annotate(
                totalCnt=Sum('totCulturalFacility')).order_by(
                'dong')
        else:
            print('{} {} 박물관/미술관 데이터 출력'.format(gu, dong))
            querySet = AddressInfo.objects.filter(gu=gu, dong=dong).values('dong').annotate(
                totalCnt=Sum('totCulturalFacility')).order_by('dong')
    for i in querySet:
        resultList.append(i['totalCnt'])
        print(i['totalCnt'])

    return myJsonResponse(resultList)


@csrf_exempt
def getRankingChartData(request, division, gu=None):
    '''
    :param request:
    :param division: rent면 월세기준, depo면 보증금 기준, rent-depo면 월세*12 + 보증금 기준
    :param gu: 있으면 해당 구의 차트 데이터 리딩
    :return: 정렬된 구, 월세, 보증금 리스트를 담은 JSON을 리턴
    '''

    guList = []
    rentalFeeList = []
    depositList = []

    if gu is None:
        for gu in seoulGu:
            totDeposit = float(0)
            totRentalFee = float(0)
            totCnt = int()
            guList.append(gu)
            print(guList)
            querySet = AddressInfo.objects.filter(gu=gu)

            for i in querySet:
                totDeposit += float(i.avgDeposit) * int(i.itemCnt)
                totRentalFee += float(i.avgRentalFee) * int(i.itemCnt)
                totCnt += i.itemCnt
            rentalFeeList.append(int(totRentalFee / totCnt))
            depositList.append(int(totDeposit / totCnt))

    else:
        querySet = AddressInfo.objects.filter(gu=gu)
        for i in querySet:
            guList.append(i.dong)
            depositList.append(int(i.avgDeposit))
            rentalFeeList.append(int(i.avgRentalFee))

    print(guList)
    print(depositList)
    print(rentalFeeList)
    # 받은 데이터를 기준으로 pandas.DataFrame 객체 생성
    data = {'gu': guList,
            'rentalFee': rentalFeeList,
            'deposit': depositList}

    rentalFeeRank = pandas.DataFrame(data)

    if division == 'rent':
        print('월세 기준 >> :::')
        rentalFeeRank['rank'] = rentalFeeRank['rentalFee'].rank(method='min', ascending=True)  # 낮은 가격순으로 순위 저장
        rentalFeeRank.sort_values(by=['rentalFee'], axis=0, inplace=True, ascending=True)  # 낮은 순위부터 정렬
    elif division == 'depo':
        print('보증금 기준 >> :::')
        rentalFeeRank['rank'] = rentalFeeRank['deposit'].rank(method='min', ascending=True)  # 낮은 가격순으로 순위 저장
        rentalFeeRank.sort_values(by=['deposit'], axis=0, inplace=True, ascending=True)  # 낮은 순위부터 정렬
    elif division == 'rent-depo':
        print('월세 1년치(12개월) + 보증금 기준 >> :::')
        rentalFeeRank['year-rent'] = rentalFeeRank['rentalFee'] * 12  # 12개월치 월세
        rentalFeeRank['rent-deposit'] = rentalFeeRank['year-rent'] + rentalFeeRank['deposit']  # 12개월치 월세 + 보증금
        rentalFeeRank['rank'] = rentalFeeRank['rent-deposit'].rank(method='min', ascending=True)  # 낮은 가격순으로 순위 저장
        rentalFeeRank.sort_values(by=['deposit'], axis=0, inplace=True, ascending=True)  # 낮은 순위부터 정렬
    else:
        return JsonResponse(data.errors, status=400)

    guList = rentalFeeRank['gu'].tolist()
    rentalFeeList = list(map(str, rentalFeeRank['rentalFee'].tolist()))
    depositList = list(map(str, rentalFeeRank['deposit'].tolist()))

    json_data = OrderedDict()
    json_data['gu'] = guList
    json_data['rentalFee'] = rentalFeeList
    json_data['deposit'] = depositList

    return myJsonResponse(json_data)


@csrf_exempt
def getTrendChartData(request, division, term, gu=None):
    '''
    :param request:
    :param division: rent면 월세, depo면 보증금 추이 차트 리딩
    :param term: 몇 개월 간의 데이터를 보여줄지 정하는 변수
    :param gu: 있으면 해당 구의 차트 데이터 리딩
    :return: 정렬된 구, 월세, 보증금 리스트를 담은 JSON을 리턴
    '''

    if gu is None:
        print("서울시 기준 ::: ")
        queryString = '''
        SELECT EXTRACT(YEAR_MONTH FROM `day`) as date, avg(rentalFee) as avg_rentalFee, avg(deposit) as avg_deposit
        FROM dataProcess_costrecord
        WHERE day >= DATE_ADD(NOW(), INTERVAL -12 MONTH)
        GROUP BY date
        ORDER BY date;
        '''
    else:
        print("%s 기준 ::: " % gu)
        queryString = '''
        SELECT EXTRACT(YEAR_MONTH FROM `day`) as date, avg(rentalFee) as avg_rentalFee, avg(deposit) as avg_deposit
        FROM dataProcess_costrecord A
        LEFT JOIN dataProcess_address B
        ON LEFT(A.houseNumber_id, 10) = B.areaCode
        WHERE day >= DATE_ADD(NOW(), INTERVAL -12 MONTH) AND gu = '%s'
        GROUP BY date
        ORDER BY date
        ''' % gu
    print("querySet ::: ", queryString)
    querySet = TrendChartData.objects.raw(queryString)

    dateList = []
    avgRentalFeeList = []
    avgDepositList = []

    for i in querySet:
        # dateList.append(i.date)
        dateShifter = str(i.date)
        dateShifter = dateShifter[0:4] + "." + dateShifter[4:6]
        dateList.append(dateShifter)
        avgRentalFeeList.append(i.avg_rentalFee)
        avgDepositList.append(i.avg_deposit)
        print(i.date, i.avg_rentalFee, i.avg_deposit)
    dateList = list(map(str, dateList))
    avgRentalFeeList = list(map(str, avgRentalFeeList))  # Decimal 형태의 index들을 단순 string으로 변환
    avgDepositList = list(map(str, avgDepositList))  # Decimal 형태의 index들을 단순 string으로 변환

    print('dateList::>>', dateList)
    print('avgRentalFeeList::>>', avgRentalFeeList)
    print('avgDepositList::>>', avgDepositList)

    json_data = OrderedDict()
    json_data['dateList'] = dateList[-term:]
    if division == 'rent':
        json_data['avgRentalFeeList'] = avgRentalFeeList[-term:]
    elif division == 'depo':
        json_data['avgDepositList'] = avgDepositList[-term:]

    return myJsonResponse(json_data)


@csrf_exempt
def getBubbleChartData(request, gu=None):
    resultList = []
    if gu is None:
        # 시 단위 데이터
        querySet = BubbleChartData.objects.filter(division='si')

    else:
        # 구 단위 데이터
        querySet = BubbleChartData.objects.filter(division=gu)

    for i in querySet:
        if i.r != 0:
            resultList.append([i.x, i.y, i.r])

    return myJsonResponse(resultList)


@csrf_exempt
def initialAddressInfo(request):
    '''
    addressInfo 테이블 초기화 메소드
    :param request:
    :return:
    '''

    queryString = '''
        SELECT * 
        FROM dataProcess_address
        ORDER BY gu, dong
    '''

    querySet = Address.objects.all().order_by('gu', 'dong')
    print('querySet:>> ', querySet)

    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(areaCode=i.areaCode)
        if created:
            print(i.gu, '데이터 존재 X!! 새로운 데이터 생성::>>')
            addressInfo.si = i.si
            addressInfo.gu = i.gu
            addressInfo.dong = i.dong
            addressInfo.avgRentalFee = 0
            addressInfo.avgDeposit = 0
            addressInfo.itemCnt = 0
            addressInfo.save()
            print(addressInfo)
        else:
            print(i.gu, '데이터 존재!! 기존 데이터 수정::>>')
            addressInfo.si = i.si
            addressInfo.gu = i.gu
            addressInfo.dong = i.dong
            addressInfo.avgRentalFee = 0
            addressInfo.avgDeposit = 0
            addressInfo.itemCnt = 0
            addressInfo.save()
            print(addressInfo)

    print('initialAddressInfo done')
    return HttpResponse('initialAddressInfo done')


@csrf_exempt
def updateAvgAddressInfo(request):
    '''
    addressInfo 테이블에 평균 월세, 보증금업데이트
    :param request:
    :return:
    '''
    queryString = '''
        select  gu, dong, avg(rentalFee) as rentalFee, avg(deposit) as deposit, count(houseNumber_id) as cnt
        from dataProcess_costrecord A
        left join dataProcess_houseinfo B
        on A.houseNumber_id = B.houseNumber
        left join dataProcess_address C
        on B.areaCode_id = C.areaCode
        GROUP BY gu, dong
        ORDER BY gu, dong
    '''
    querySet = Average.objects.raw(queryString)  # 각 동별 평균 월세, 보증금 계산

    print('querySet:>> ', querySet)

    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.avgDeposit = i.deposit
        addressInfo.avgRentalFee = i.rentalFee
        addressInfo.itemCnt = i.cnt
        addressInfo.save()
        print(addressInfo)

    print('updateAvgAddressInfo done')
    return HttpResponse('updateAvgAddressInfo done')


@csrf_exempt
def updateBubbleChartData(request):
    # 월세를 10만원 단위로 나눠보자
    print('{} bubbleChartData Update...'.format('서울시'))
    BubbleChartData.objects.filter(division='si').delete()  # 업데이트 전 삭제
    for rent in range(0, 100, 10):
        minRentalFee = rent
        maxRentalFee = rent + 9
        querySet = CostRecord.objects.filter(rentalFee__range=(minRentalFee, maxRentalFee))

        houseNumberList = []
        rentalFeeList = []
        depositList = []

        for i in querySet:
            houseNumberList.append(i.houseNumber)
            rentalFeeList.append(i.rentalFee)
            depositList.append(i.deposit)
            # print(j.houseNumber, j.rentalFee, j.deposit)

        data = {
            'houseNumber': houseNumberList,
            'rentalFee': rentalFeeList,
            'deposit': depositList
        }
        rentalFeeRank = pandas.DataFrame(data)  # 해당 월세 범위에 해당하는 매물들로 dataFrame생성.

        # 이제 보증금 단위로 나눠보자.
        for depo in range(1000, 4000, 500):
            minDeposit = depo
            maxDeposit = depo + 500
            temp = rentalFeeRank[(rentalFeeRank["deposit"] >= minDeposit) & (rentalFeeRank["deposit"] < maxDeposit)]
            # print("{}이상 {}미만 : {}".format(start, end, temp.size))

            print("x:{} y:{} r:{}".format(rent, depo, temp.size))
            # 시단위
            bubbleChartData = BubbleChartData.objects.create(x=maxRentalFee + 1, y=maxDeposit, r=temp.size,
                                                             division='si')

            # print(j.costRecordId, j.rentalFee)

    for curGu in seoulGu:
        # 월세를 10만원 단위로 나눠보자.
        print('{} bubbleChartData Update...'.format(curGu))
        BubbleChartData.objects.filter(division=curGu).delete()  # 업데이트 전 삭제
        for rent in range(0, 100, 10):
            minRentalFee = rent
            maxRentalFee = rent + 9
            queryString = '''
                select day, rentalFee, deposit, houseNumber_id, costRecordId from dataProcess_costrecord
                left join dataProcess_houseinfo
                on dataProcess_costrecord.houseNumber_id = dataProcess_houseinfo.houseNumber
                left join dataProcess_address
                on dataProcess_houseinfo.areaCode_id = dataProcess_address.areaCode
                where gu= '{}' AND rentalFee between {} AND {}
            '''.format(curGu, minRentalFee, maxRentalFee)  # 여기 최소값 최대값 where조건에 넣어줘야햄

            querySet = CostRecord.objects.raw(queryString)

            houseNumberList = []
            rentalFeeList = []
            depositList = []

            for i in querySet:
                houseNumberList.append(i.houseNumber)
                rentalFeeList.append(i.rentalFee)
                depositList.append(i.deposit)

            data = {
                'houseNumber': houseNumberList,
                'rentalFee': rentalFeeList,
                'deposit': depositList
            }
            rentalFeeRank = pandas.DataFrame(data)  # 해당 월세 범위에 해당하는 매물들로 dataFrame생성.

            # 이제 보증금 단위로 나눠보자.
            for depo in range(1000, 4000, 500):
                minDeposit = depo
                maxDeposit = depo + 500
                temp = rentalFeeRank[(rentalFeeRank["deposit"] >= minDeposit) & (rentalFeeRank["deposit"] < maxDeposit)]

                print("gu:{} x:{} y:{} r:{}".format(curGu, rent, depo, temp.size))
                # 구단위
                bubbleChartData = BubbleChartData.objects.create(x=maxRentalFee + 1, y=maxDeposit, r=temp.size,
                                                                 division=curGu)

    return HttpResponse("updateBubbleChartData done")


@csrf_exempt
def getPieChartData(request, gu, dong):
    '''
    각 항목별 지수 계산기
    '''
    addressInfo = AddressInfo.objects.filter(gu=gu, dong=dong)
    decimalPlaces = 4  # 소숫점 이하 자리수
    # 치안
    safety_data = OrderedDict()
    safety_data['CCTV'] = round(addressInfo[0].rateCCTV, decimalPlaces)
    safety_data['보안등'] = round(addressInfo[0].rateLight, decimalPlaces)
    safety_data['경찰시설'] = round(addressInfo[0].ratePolice, decimalPlaces)

    # 생활
    life_data = OrderedDict()
    life_data['약국'] = round(addressInfo[0].ratePharmacy, decimalPlaces)
    life_data['시장'] = round(addressInfo[0].rateMarket, decimalPlaces)
    life_data['공원'] = round(addressInfo[0].ratePark, decimalPlaces)

    # 문화
    culture_data = OrderedDict()
    culture_data['체육시설'] = round(addressInfo[0].rateGym, decimalPlaces)
    culture_data['공연장'] = round(addressInfo[0].rateConcertHall, decimalPlaces)
    culture_data['도서관'] = round(addressInfo[0].rateLibrary, decimalPlaces)
    culture_data['박물관/미술관'] = round(addressInfo[0].rateCulturalFacility, decimalPlaces)

    # 교통
    trans_data = OrderedDict()
    trans_data['지하철'] = round(addressInfo[0].rateSubway, decimalPlaces)
    trans_data['버스'] = round(addressInfo[0].rateBus, decimalPlaces)

    json_data = OrderedDict()
    json_data['치안'] = safety_data
    json_data['생활'] = life_data
    json_data['문화'] = culture_data
    json_data['교통'] = trans_data

    return myJsonResponse(json_data)


@csrf_exempt
def updateTotsAddressInfo(request):
    '''
    update CCTV, PoliceOffice, SercurityLight, Pharmacy, Market, Park, Gym, ConcertHall, Library, CulturalFacility, Subway, Bus
    '''

    # CCTV
    querySet = Result_GuDongCnt.objects.raw('''
        select gu, dong, count(cctvId) as cnt
        from dataProcess_address A
        left outer join dataProcess_cctv B
        on A.areaCode = B.areaCode_id
        group by gu, dong
        order by gu, dong
        ''')
    print("CCTV querySet ::: ", querySet)
    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.totCCTV = i.cnt
        addressInfo.save()

    # PoliceOffice
    querySet = Result_GuDongCnt.objects.raw('''
        select gu, dong, count(policeId) as cnt
        from dataProcess_address A
        left outer join dataProcess_policeoffice B
        on A.areaCode = B.areaCode_id
        group by gu, dong
        order by gu, dong
        ''')
    print("PoliceOffice querySet ::: ", querySet)
    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.totPolice = i.cnt
        addressInfo.save()

    # SecurityLight
    querySet = Result_GuDongCnt.objects.raw('''
        select gu, dong, count(lightId) as cnt
        from dataProcess_address A
        left outer join dataProcess_securitylight B
        on A.areaCode = B.areaCode_id
        group by gu, dong
        order by gu, dong
        ''')
    print("SecurityLight querySet ::: ", querySet)
    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.totLight = i.cnt
        addressInfo.save()

    # Pharmacy
    querySet = Result_GuDongCnt.objects.raw('''
        select gu, dong, count(pharmacyId) as cnt
        from dataProcess_address A
        left outer join dataProcess_pharmacy B
        on A.areaCode = B.areaCode_id
        group by gu, dong
        order by gu, dong
        ''')
    print("Pharmacy querySet ::: ", querySet)
    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.totPharmacy = i.cnt
        addressInfo.save()

    # Market
    querySet = Result_GuDongCnt.objects.raw('''
        select gu, dong, count(marketId) as cnt
        from dataProcess_address A
        left outer join dataProcess_market B
        on A.areaCode = B.areaCode_id
        group by gu, dong
        order by gu, dong
        ''')
    print("Market querySet ::: ", querySet)
    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.totMarket = i.cnt
        addressInfo.save()

    # Park
    querySet = Result_GuDongCnt.objects.raw('''
        select gu, dong, count(parkId) as cnt
        from dataProcess_address A
        left outer join dataProcess_park B
        on A.areaCode = B.areaCode_id
        group by gu, dong
        order by gu, dong
        ''')
    print("Park querySet ::: ", querySet)
    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.totPark = i.cnt
        addressInfo.save()

    # Gym
    querySet = Result_GuDongCnt.objects.raw('''
        select gu, dong, count(gymId) as cnt
        from dataProcess_address A
        left outer join dataProcess_gym B
        on A.areaCode = B.areaCode_id
        group by gu, dong
        order by gu, dong
        ''')
    print("Gym querySet ::: ", querySet)
    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.totGym = i.cnt
        addressInfo.save()

    # ConcertHall
    querySet = Result_GuDongCnt.objects.raw('''
        select gu, dong, count(concertHallId) as cnt
        from dataProcess_address A
        left outer join dataProcess_concerthall B
        on A.areaCode = B.areaCode_id
        group by gu, dong
        order by gu, dong
        ''')
    print("ConcertHall querySet ::: ", querySet)
    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.totConcertHall = i.cnt
        addressInfo.save()

    # Library
    querySet = Result_GuDongCnt.objects.raw('''
        select gu, dong, count(libraryId) as cnt
        from dataProcess_address A
        left outer join dataProcess_library B
        on A.areaCode = B.areaCode_id
        group by gu, dong
        order by gu, dong
        ''')
    print("Library querySet ::: ", querySet)
    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.totLibrary = i.cnt
        addressInfo.save()

    # CulturalFacility
    querySet = Result_GuDongCnt.objects.raw('''
        select gu, dong, count(culturalFacilityId) as cnt
        from dataProcess_address A
        left outer join dataProcess_culturalfacility B
        on A.areaCode = B.areaCode_id
        group by gu, dong
        order by gu, dong
        ''')
    print("CulturalFacilsity querySet ::: ", querySet)

    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.totCulturalFacility = i.cnt
        addressInfo.save()

    # Subway
    querySet = Result_GuDongCnt.objects.raw('''
        select gu, dong, count(id) as cnt
        from dataProcess_address A
        left outer join dataProcess_subway B
        on A.areaCode = B.areaCode_id
        group by gu, dong
        order by gu, dong
        ''')
    print("Subway querySet ::: ", querySet)

    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.totSubway = i.cnt
        addressInfo.save()

    # Bus
    querySet = Result_GuDongCnt.objects.raw('''
        select gu, dong, count(id) as cnt
        from dataProcess_address A
        left outer join dataProcess_bus B
        on A.areaCode = B.areaCode_id
        group by gu, dong
        order by gu, dong
        ''')
    print("Bus querySet ::: ", querySet)

    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.totBus = i.cnt
        addressInfo.save()

    return HttpResponse("updateTotsAddressInfo done")


@csrf_exempt
def updateRatesAddressInfo(request):
    '''
    각 항목별 지수 계산하는 함수
    '''
    file_Path = os.path.join(settings.BASE_DIR, "STCService")
    areaJsonData = json.loads(open(os.path.join(file_Path, "법정동별면적.json"), "r", encoding='utf8').read())

    siArea = float(areaJsonData['전체'])  # 임시 서울 시 전체 면적 :: api로 받아오자.
    guArea = float()  # 임시 동 전체 면적
    totSumList = AddressInfo.objects.aggregate(
        Sum('totCCTV'),
        Sum('totPolice'),
        Sum('totLight'),
        Sum('totPharmacy'),
        Sum('totMarket'),
        Sum('totPark'),
        Sum('totGym'),
        Sum('totConcertHall'),
        Sum('totLibrary'),
        Sum('totCulturalFacility'),
        Sum('totBus'),
        Sum('totSubway'))

    addressInfoQuerySet = AddressInfo.objects.all()

    for curDong in addressInfoQuerySet:
        guArea = float(areaJsonData[curDong.gu][curDong.dong])  # 1은 임시 데이터!! 여기서 curDong를가지고 api로 해당 guArea를 가져옴.
        # 그리고나서 각 항목들의 rate를 계산.

        # rateCCTV 계산
        if totSumList['totCCTV__sum'] == 0:
            curDong.rateCCTV = 0
        else:
            curDong.rateCCTV = (curDong.totCCTV / guArea) / (totSumList['totCCTV__sum'] / siArea)

        # ratePolice 계산
        if totSumList['totPolice__sum'] == 0:
            curDong.ratePolice = 0
        else:
            curDong.ratePolice = (curDong.totPolice / guArea) / (totSumList['totPolice__sum'] / siArea)

        # rateLight 계산
        if totSumList['totLight__sum'] == 0:
            curDong.rateLight = 0
        else:
            curDong.rateLight = (curDong.totLight / guArea) / (totSumList['totLight__sum'] / siArea)

        # ratePharmacy 계산
        if totSumList['totPharmacy__sum'] == 0:
            curDong.ratePharmacy = 0
        else:
            curDong.ratePharmacy = (curDong.totPharmacy / guArea) / (totSumList['totPharmacy__sum'] / siArea)

        # rateMarket 계산
        if totSumList['totMarket__sum'] == 0:
            curDong.rateMarket = 0
        else:
            curDong.rateMarket = (curDong.totMarket / guArea) / (totSumList['totMarket__sum'] / siArea)

        # ratePark 계산
        if totSumList['totPark__sum'] == 0:
            curDong.ratePark = 0
        else:
            curDong.ratePark = (curDong.totPark / guArea) / (totSumList['totPark__sum'] / siArea)

        # rateGym 계산
        if totSumList['totGym__sum'] == 0:
            curDong.rateGym = 0
        else:
            curDong.rateGym = (curDong.totGym / guArea) / (totSumList['totGym__sum'] / siArea)

        # rateConcertHall 계산
        if totSumList['totConcertHall__sum'] == 0:
            curDong.rateConcertHall = 0
        else:
            curDong.rateConcertHall = (curDong.totConcertHall / guArea) / (totSumList['totConcertHall__sum'] / siArea)

        # rateLibrary 계산
        if totSumList['totLibrary__sum'] == 0:
            curDong.rateLibrary = 0
        else:
            curDong.rateLibrary = (curDong.totLibrary / guArea) / (totSumList['totLibrary__sum'] / siArea)

        # rateCulturalFacility 계산
        if totSumList['totCulturalFacility__sum'] == 0:
            curDong.rateCulturalFacility = 0
        else:
            curDong.rateCulturalFacility = (curDong.totCulturalFacility / guArea) / (
                    totSumList['totCulturalFacility__sum'] / siArea)

        # rateBus 계산
        if totSumList['totBus__sum'] == 0:
            curDong.rateBus = 0
        else:
            curDong.rateBus = (curDong.totBus / guArea) / (totSumList['totBus__sum'] / siArea)

        # rateSubway 계산
        if totSumList['totSubway__sum'] == 0:
            curDong.rateSubway = 0
        else:
            curDong.rateSubway = (curDong.totSubway / guArea) / (totSumList['totSubway__sum'] / siArea)
        curDong.save()

    print("rate 가공 시작 ::")
    addressInfoQuerySet = AddressInfo.objects.all()

    guList = []
    dongList = []
    rateCCTVList = []
    ratePoliceList = []
    rateLightList = []
    ratePharmacyList = []
    rateMarketList = []
    rateParkList = []
    rateGymList = []
    rateConcertHallList = []
    rateLibraryList = []
    rateCulturalFacilityList = []
    rateSubwayList = []
    rateBusList = []

    for i in addressInfoQuerySet:
        guList.append(i.gu)
        dongList.append(i.dong)
        rateCCTVList.append(i.rateCCTV)
        ratePoliceList.append(i.ratePolice)
        rateLightList.append(i.rateLight)
        ratePharmacyList.append(i.ratePharmacy)
        rateMarketList.append(i.rateMarket)
        rateParkList.append(i.ratePark)
        rateGymList.append(i.rateGym)
        rateConcertHallList.append(i.rateConcertHall)
        rateLibraryList.append(i.rateLibrary)
        rateCulturalFacilityList.append(i.rateCulturalFacility)
        rateSubwayList.append(i.rateSubway)
        rateBusList.append(i.rateBus)

    data = {
        'rateCCTV': rateCCTVList,
        'ratePolice': ratePoliceList,
        'rateLight': rateLightList,
        'ratePharmacy': ratePharmacyList,
        'rateMarket': rateMarketList,
        'ratePark': rateParkList,
        'rateGym': rateGymList,
        'rateConcertHall': rateConcertHallList,
        'rateLibrary': rateLibraryList,
        'rateCulturalFacility': rateCulturalFacilityList,
        'rateSubway': rateSubwayList,
        'rateBus': rateBusList
    }
    df = pandas.DataFrame(data, index=[guList, dongList])

    df2 = df.copy()
    df2[:] = MinMaxScaler().fit_transform(df2[:])  # 정규화 진행

    for i in range(0, len(df2)):
        curRow = df2.iloc[i]
        print('구: {} // 동: {} rateData Update ::'.format(curRow.name[0], curRow.name[1]))
        changeQuery, created = AddressInfo.objects.get_or_create(gu=curRow.name[0], dong=curRow.name[1])
        changeQuery.rateCCTV = curRow.rateCCTV
        changeQuery.ratePolice = curRow.ratePolice
        changeQuery.rateLight = curRow.rateLight
        changeQuery.ratePharmacy = curRow.ratePharmacy
        changeQuery.rateMarket = curRow.rateMarket
        changeQuery.ratePark = curRow.ratePark
        changeQuery.rateGym = curRow.rateGym
        changeQuery.rateConcertHall = curRow.rateConcertHall
        changeQuery.rateLibrary = curRow.rateLibrary
        changeQuery.rateCulturalFacility = curRow.rateCulturalFacility
        changeQuery.rateSubway = curRow.rateSubway
        changeQuery.rateBus = curRow.rateBus
        changeQuery.save()

        print('rate 가공 완료')

    return HttpResponse("updateRatesAddressInfo done")


# dummyData ↓↓↓
@csrf_exempt
def getDummyDataForDH(request, div):
    if div == 1:
        print('div = 1 ::')
        dummyData = '''
            {
      "": [
        {
          "rank": 1,
          "address": "서울시 강북구 번동",
          "latitude": 37.641421,
          "longitude": 127.030254
        },
        {
          "rank": 2,
          "address": "서울특별시 송파구 잠실본동",
          "latitude": 37.507262,
          "longitude": 127.08339
        },
        {
          "rank": 3,
          "address": "서울 종로구 종로5길",
          "latitude": 37.590827,
          "longitude": 126.978347
        },
        {
          "rank": 4,
          "address": "서울 광진구 아차산로33길 21-5",
          "latitude": 37.541336,
          "longitude": 127.06765
        },
        {
          "rank": 5,
          "address": "서울 성북구 보문로34길",
          "latitude": 37.507262,
          "longitude": 127.015587
        },
        {
          "rank": 6,
          "address": "서울 강남구 삼성로104길 23 성지빌딩",
          "latitude": 37.51132,
          "longitude": 127.054379
        },
        {
          "rank": 7,
          "address": "서울 강북구 월계로7나길 50",
          "latitude": 37.61316,
          "longitude": 127.029252
        },
        {
          "rank": 8,
          "address": "서울 광진구 동일로18길 52",
          "latitude": 37.539101,
          "longitude": 127.065628
        },
        {
          "rank": 9,
          "address": "서울 종로구 북촌로4길 19 1층",
          "latitude": 37.579424,
          "longitude": 126.984057
        },
        {
          "rank": 10,
          "address": "서울 성동구 서울숲2길 40-7 1층 엘더버거",
          "latitude": 37.546264,
          "longitude": 127.040826
        }
      ]
    }
    '''
    elif div == 2:
        print('div = 2 ::')
        dummyData = '''
                    [
                    {
          "labels": [
                "예산",
                "치안",
                "생활",
                "문화",
                "교통"
              ],
          "status": [
            {
              "rank": 1,
              "address": "서울시 강북구 번동",
              "budget": 35,
              "safety": 44,
              "life": 37,
              "culture": 48,
              "traffic": 50
            },
            {
              "rank": 2,
              "address": "서울특별시 송파구 잠실본동",
              "budget": 60,
              "safety": 47,
              "life": 34,
              "culture": 24,
              "traffic": 64
            },
            {
              "rank": 3,
              "address": "서울 종로구 종로5길",
              "budget": 34,
              "safety": 54,
              "life": 63,
              "culture": 46,
              "traffic": 27
            },
            {
              "rank": 4,
              "address": "서울 광진구 아차산로33길 21-5",
              "budget": 34,
              "safety": 64,
              "life": 53,
              "culture": 23,
              "traffic": 54
            },
            {
              "rank": 5,
              "address": "서울 성북구 보문로34길",
              "budget": 24,
              "safety": 34,
              "life": 54,
              "culture": 53,
              "traffic": 63
            },
            {
              "rank": 6,
              "address": "서울 강북구 월계로7나길 50",
              "budget": 63,
              "safety": 42,
              "life": 83,
              "culture": 35,
              "traffic": 64
            },
            {
              "rank": 7,
              "address": "서울 광진구 동일로18길 52",
              "budget": 26,
              "safety": 74,
              "life": 35,
              "culture": 46,
              "traffic": 37
            },
            {
              "rank": 8,
              "address": "서울 종로구 북촌로4길 19 1층",
              "budget": 37,
              "safety": 74,
              "life": 63,
              "culture": 45,
              "traffic": 60
            },
            {
              "rank": 9,
              "address": "서울 성동구 서울숲2길 40-7 1층 엘더버거",
              "budget": 45,
              "safety": 36,
              "life": 74,
              "culture": 54,
              "traffic": 43
            },
            {
              "rank": 10,
              "address": "서울시 강북구 번동",
              "budget": 54,
              "safety": 64,
              "life": 35,
              "culture": 46,
              "traffic": 36
            }
          ]
        }
        ]

    '''
    elif div == 3:
        print('div = 3 ::')
        dummyData = '''
            {
              "labels": [
                "예산",
                "치안",
                "생활",
                "문화",
                "교통"
              ],
              "username": "김다현",
              "dataset": [
                {
                  "budget": 54,
                  "safety": 47,
                  "life": 34,
                  "culture": 24,
                  "traffic": 64
                }
              ]
            }
        '''
    else:
        return HttpResponse("잘못된 url입력입니다.")

    return HttpResponse(dummyData)


@csrf_exempt
def saveFrequentPlace(request):
    '''
    :param request:
    :return:
    '''
    request = json.loads(request.body)

    memberId = request['id']
    latitude = request['latitude']
    longitude = request['longitude']
    PlaceName = request['placeName']
    gu = request['gu']
    dong = request['dong']

    querySet, created = FrequentPlace.objects.get_or_create(
        id=Member.objects.get(id=memberId),
        latitude=latitude,
        longitude=longitude,
        placeName=PlaceName,
        areaCode=Address.objects.get(gu=gu, dong=dong)
    )
    querySet.save()
    # return 해주는건 수정
    return HttpResponse("SaveFrequentPlace done")
    # return myJsonResponse(json_data)


# dummyData ↑↑↑

########################## ↑↑↑↑↑↑↑↑ ############################

##### 메모장..
# for gu, gu_areaCode in seoulGu.items():  # Dict형 key, value읽어오기
# query = 'SELECT * FROM myapp_person WHERE last_name = %s' % gu

# group by 할 필드를 values안에 넣자.
# querySet = AddressInfo.objects.values('gu').annotate(totalCnt=Sum('totCCTV')).values('totalCnt')

# ORM 특정 필드의 SUM 구하기.
# totSumList = AddressInfo.objects.aggregate(Sum('totCCTV'))
##### 메모장..

# ########################### ↓↓↓↓테스트 코드↓↓↓↓ ###########################
@csrf_exempt
def testQuery(request):
    '''
    :param request:
    :return:
    '''
    request = json.loads(request.body)

    memberId = request['id']
    latitude = request['latitude']
    longitude = request['longitude']
    PlaceName = request['placeName']
    gu = request['gu']
    dong = request['dong']

    querySet, created = FrequentPlace.objects.get_or_create(
        id=Member.objects.get(id=memberId),
        latitude=latitude,
        longitude=longitude,
        placeName=PlaceName,
        areaCode=Address.objects.get(gu=gu, dong=dong)
    )
    querySet.save()
    # return 해주는건 수정
    return HttpResponse("SaveFrequentPlace done")
    # return myJsonResponse(json_data)


# def testQuery2(request):  # 각 구별 월세, 보증금 데이터 읽기.
#     # 분석을 위해 pandas DataFrame 구조로 변환까지 완료
#
#     querySet = Average.objects.raw('''
#     SELECT gu , avg(rentalFee) as rentalFee, avg(deposit) as deposit
#     FROM dataProcess_address A
#     LEFT OUTER JOIN dataProcess_costrecord B
#     ON A.areaCode = left(B.houseNumber_id, 10)
#     GROUP BY gu
#     ORDER BY gu
#     ''')
#     guList = []
#     rentalFeeList = []
#     depositList = []
#
#     for i in querySet:
#         guList.append(i.gu)
#         rentalFeeList.append(i.rentalFee)
#         depositList.append(i.deposit)
#
#         print(i.gu, i.rentalFee, i.deposit)
#
#     data = {'rentalFee': rentalFeeList,
# #             'deposit': depositList}
# #
# #     df = pandas.DataFrame(data, index=guList)
#
#     for i in df:
#         print(df)
#
#     return myJsonResponse(querySet)


# ########################### ↑↑↑↑테스트 코드↑↑↑↑ ###########################


##################### ↓↓↓↓ 당장에 안쓰는 메소드 ↓↓↓↓ #####################
def findGuAreaCodes(gu):
    """
    :param gu: 검색을 원하는 구 이름
    :return: 해당 구 내의 모든 행정동 areaCode 값 배열 (문자열 배열)
    """

    print(">> findGuAreaCodes 함수 호출")
    areaCodeArr = []  # 빈 배열 생성
    addresses = Address.objects.filter(gu=gu)  # 해당 구 이름으로 검색된 Address 객체집합
    for i in addresses:
        areaCodeArr.append(i.areaCode)  # Address 객체집합을 돌면서 areaCode만 areaCodeArr배열에 저장
    print("==== " + gu + " areaCode 배열 완성 ====")
    print(">> findGuAreaCodes 함수 종료")
    return areaCodeArr


@csrf_exempt
def getCCTVInfosByGu(gu=None):  # 입력한 gu에 있는 CCTV 검색
    """
    :param gu: 검색을 원하는 구 이름
    :return: 해당 구 내의 모든 CCTV 배열 (CCTV 객체)
    """

    resultArr = []  # CCTV들을 받아내는 최종 결과 배열
    areaCodeArr = findGuAreaCodes(gu)  # 해당 gu의 areaCode들 검색

    TOT = queryResult = CCTV.objects.filter(
        areaCode=areaCodeArr[0])
    for i in TOT:
        resultArr.append(i)  # 그 결과값들을 resultArr에 붙여서 저장한다.

    for currentAreaCode in areaCodeArr[1:]:
        queryResult = CCTV.objects.filter(
            areaCode=currentAreaCode)  # 해당 areaCode로 검색된 결과(CCTV)를 queryResult에 저장
        for i in queryResult:
            resultArr.append(i)  # 그 결과값들을 resultArr에 붙여서 저장한다.
        TOT = TOT | queryResult

    print("finally :: ")
    for i in resultArr:
        # 확인을 위한 CCTV 정보 출력
        print(i.cctvId, i.areaCode_id, i.latitude, i.longitude)

    serializer = HouseInfoSerializer(TOT, many=True)
    finalResult = JsonResponse({gu: serializer.data}, safe=False)  # <class 'django.http.response.JsonResponse'>
    return finalResult


@csrf_exempt
def getSecurityLightInfosByGu(gu=None):  # 입력한 gu에 있는 보안등 검색
    """
    :param gu: 검색을 원하는 구 이름
    :return: 해당 구 내의 모든 SecurityLight 배열 (SecurityLight 객체)
    """

    resultArr = []  # 보안등들을 받아내는 최종 결과 배열
    areaCodeArr = findGuAreaCodes(gu)  # 해당 gu의 areaCode들 검색

    TOT = queryResult = SecurityLight.objects.filter(
        areaCode=areaCodeArr[0])
    for i in TOT:
        resultArr.append(i)  # 그 결과값들을 resultArr에 붙여서 저장한다.

    for currentAreaCode in areaCodeArr[1:]:
        queryResult = SecurityLight.objects.filter(
            areaCode=currentAreaCode)  # 해당 areaCode로 검색된 결과(보안등)를 queryResult에 저장
        for i in queryResult:
            resultArr.append(i)  # 그 결과값들을 resultArr에 붙여서 저장한다.
        TOT = TOT | queryResult

    print("finally :: ")
    for i in resultArr:
        # 확인을 위한 보안등 정보 출력
        print(i.lightId, i.areaCode_id, i.latitude, i.longitude)

    serializer = HouseInfoSerializer(TOT, many=True)
    finalResult = JsonResponse({gu: serializer.data}, safe=False)  # <class 'django.http.response.JsonResponse'>
    return finalResult


@csrf_exempt
def getPoliceOfficeInfosByGu(gu=None):  # 입력한 gu에 있는 경찰시설 검색
    """
    :param gu: 검색을 원하는 구 이름
    :return: 해당 구 내의 모든 PoliceOffice 배열 (PoliceOffice 객체)
    """

    resultArr = []  # 경찰시설들을 받아내는 최종 결과 배열
    areaCodeArr = findGuAreaCodes(gu)  # 해당 gu의 areaCode들 검색

    TOT = queryResult = PoliceOffice.objects.filter(
        areaCode=areaCodeArr[0])
    for i in TOT:
        resultArr.append(i)  # 그 결과값들을 resultArr에 붙여서 저장한다.

    for currentAreaCode in areaCodeArr[1:]:
        queryResult = PoliceOffice.objects.filter(
            areaCode=currentAreaCode)  # 해당 areaCode로 검색된 결과(경찰시설)를 queryResult에 저장
        for i in queryResult:
            resultArr.append(i)  # 그 결과값들을 resultArr에 붙여서 저장한다.
        TOT = TOT | queryResult

    print("finally :: ")
    for i in resultArr:
        # 확인을 위한 경찰시설 정보 출력
        print(i.policeId, i.areaCode_id, i.latitude, i.longitude, i.policeOfficeName)

    serializer = HouseInfoSerializer(TOT, many=True)
    finalResult = JsonResponse({gu: serializer.data}, safe=False)  # <class 'django.http.response.JsonResponse'>
    return finalResult


##################### ↑↑↑↑ 당장에 안쓰는 메소드 ↑↑↑↑ #####################

######################### Login ####################################
'''
def kakaoJoin(request):
    accessToken = request.headers["AccessToken"]
    baseUrl = "https://kapi.kakao.com/v2/user/me"
    authorization = "Bearer " + accessToken
    propertyKeys = ["properties.nickname", "kakao_account.age_range", "kakao_account.gender"]
    print(str(propertyKeys))

    http = httplib2.Http()

    response, content = http.request(baseUrl, method="POST", headers={"Authorization": authorization},
                                     body="property_keys=" + str(propertyKeys))

    content = content.decode("utf-8")
    jsonData = json.loads(content)
    print(jsonData)

    id = jsonData["id"]
    if Member.objects.filter(id=id).count == 0:
        password = ""
        name = jsonData["properties"]["nickname"]
        if jsonData["kakao_account"]["email_needs_agreement"] == "False" and jsonData["kakao_account"][
            "is_email_valid"] == "True":
            email = jsonData["kakao_account"]["email"]
            member = Member(id=id, email=email, password=password, name=name)
            member.save()

            memberInfo = MemberInfo(member=member, gender=None, age_range=None, rentalFee=None, deposit=None)

            if (jsonData["kakao_account"]["age_range_needs_agreement"] == "False" and jsonData["kakao_account"][
                "has_age_range"] == "True"):
                age_range = jsonData["kakao_account"]["age_range"]
                setattr(memberInfo, "age_range", age_range)

            if (jsonData["kakao_account"]["gender_needs_agreement"] == "False" and jsonData["kakao_account"][
                "has_gender"] == "True"):
                gender = jsonData["kakao_account"]["gender"]
                setattr(memberInfo, "gender", gender)

            memberInfo.save()

    return HttpResponse(jsonData)
'''
'''
def join(request):
    id = request.headers["id"]
    email = request.headers["email"]
    password = request.headers["password"]
    name = request.headers["name"]
    if Member.objects.filter(id=id).count() == 0 and Member.objects.filter(email=email).count() == 0:
        member = Member(id=id, email=email, password=password, name=name)
        member.save()

        memberInfo = MemberInfo(member=member, gender=None, age_range=None, rentalFee=None, deposit=None)
        if "gender" in request.headers:
            gender = request.headers["gender"]
            setattr(memberInfo, "gender", gender)

        if "age_range" in request.headers:
            age_range = request.headers["age_range"]
            setattr(memberInfo, "age_range", age_range)

        if "rentalFee" in request.headers:
            rentalFee = request.headers["rentalFee"]
            setattr(memberInfo, "rentalFee", rentalFee)

        if "deposit" in request.headers:
            deposit = request.headers["deposit"]
            setattr(memberInfo, "deposit", deposit)

        memberInfo.save()

        memberTrend = MemberTrend(member=member)
        memberTrend.save()

        return HttpResponse("join success")
    return HttpResponse("id or email is already exist")
'''
'''
def login(request):
    id = request.headers["id"]
    password = request.headers["password"]

    if Member.objects.filter(id=id, password=password):
        return HttpResponse("login success")
    else:
        return HttpResponse("login fail")
'''

def count(request, id, category, milliseconds):
    m = 1000
    if 2 * m < milliseconds < 60 * m:
        if MemberTrend.objects.filter(member_id=id).count() == 1:
            memberTrend = MemberTrend.objects.get(member_id=id)
            setattr(memberTrend, category, getattr(memberTrend, category) + 1)
            memberTrend.save()
        else:
            if TrendBySession.objects.filter(sessionId=id).count() == 1:
                trendBySession = TrendBySession.objects.get(sessionId=id)
            else:
                trendBySession = TrendBySession(sessionId=id)

            setattr(trendBySession, category, getattr(trendBySession, category) + 1)
            trendBySession.save()
        return HttpResponse("count success")

    return HttpResponse("count failed : " + str(milliseconds) + " milliseconds in " + category + " category")


def recommendation(request):
    memberId = request.headers["memberId"]
    memberTrend = MemberTrend.objects.get(member_id__memberId=memberId)

    trends = {"budget": memberTrend.budget, "safety": memberTrend.safety, "life": memberTrend.life,
              "culture": memberTrend.culture, "transportation": memberTrend.transportation}

    trendsSorted = sorted(trends.items(), key=(lambda x: x[1]), reverse=True)
    points = setPoint(trendsSorted)


    addresses = AddressInfo.objects.all().annotate(
        budget = ((F("avgRentalFee") * 12) + F("avgDeposit")) / 100 * points["budget"],
        safety = (F("rateCCTV") + F("ratePolice") + F("rateLight")) * points["safety"] / 3,
        life = (F("ratePharmacy") + F("rateMarket") + F("ratePark") + F("rateGym")) * points["life"] / 4,
        culture = (F("rateConcertHall") + F("rateLibrary") + F("rateCulturalFacility")) * points["culture"] / 3,
        transportation = (F("rateSubway") + F("rateBus")) * points["transportation"] / 2,
        mean = (F("budget") + F("safety") + F("life") + F("culture") + F("transportation")) / 5
    ).values("areaCode", "budget", "safety", "life", "culture", "transportation", "mean").order_by("-mean")

    dongs = []
    for i in range(0, 5):
        areaCode = Address.objects.get(areaCode=addresses[i]["areaCode"])
        pointOfBudget = addresses[i]["budget"]
        pointOfSafety = addresses[i]["safety"]
        pointOfLife = addresses[i]["life"]
        pointOfCulture = addresses[i]["culture"]
        pointOfTransportation = addresses[i]["transportation"]
        dong = RecommendedDong(areaCode=areaCode, pointOfBudget=pointOfBudget, pointOfSafety=pointOfSafety,
                        pointOfLife=pointOfLife, pointOfCulture=pointOfCulture,
                        pointOfTransportation=pointOfTransportation)
        dong.save()
        dongs.append(dong)

    if Recommendation.objects.filter(memberTrend=memberTrend).count() == 0:
        recommendation = Recommendation(memberTrend=memberTrend, pointOfBudget=points["budget"], pointOfSafety=points["safety"],
                                        pointOfLife=points["life"], pointOfCulture=points["culture"], pointOfTransportation=points["transportation"],
                                        dong1=dongs[0], dong2=dongs[1], dong3=dongs[2], dong4=dongs[3], dong5=dongs[4])
    else:
        recommendation = Recommendation.objects.get(memberTrend=memberTrend)
        setattr(recommendation, "pointOfBudget", points["budget"])
        setattr(recommendation, "pointOfSafety", points["safety"])
        setattr(recommendation, "pointOfLife", points["life"])
        setattr(recommendation, "pointOfCulture", points["culture"])
        setattr(recommendation, "pointOfTransportation", points["transportation"])
        setattr(recommendation, "dong1", dongs[0])
        setattr(recommendation, "dong2", dongs[1])
        setattr(recommendation, "dong3", dongs[2])
        setattr(recommendation, "dong4", dongs[3])
        setattr(recommendation, "dong5", dongs[4])

    recommendation.save()

    return HttpResponse("추천 끝")


def setPoint(trendsSorted):
    curTrend = trendsSorted[0][1]
    cnt = 0
    trendsPoints = {}
    point = len(trendsSorted)
    for trend in trendsSorted:
        if trend[1] == curTrend:
            cnt += 1
        else:
            curTrend = trend[1]
            point -= cnt
            cnt = 1
        trendsPoints[trend[0]] = point

    return trendsPoints

def getRecommendedDongList(request):
    memberId = request.headers["memberId"]
    recommendation = Recommendation.objects.select_related("memberTrend")\
        .select_related("dong1").select_related("dong2").select_related("dong3")\
        .select_related("dong4").select_related("dong5").get(memberTrend__member_id=memberId)

    dongs = [recommendation.dong1, recommendation.dong2, recommendation.dong3, recommendation.dong4, recommendation.dong5]
    dongToSend = []
    for i, dong in enumerate(dongs, 1):
        address = Address.objects.get(areaCode=dong.areaCode)
        info = {
            "rank" : i,
            "address" : address.si + " " + address.gu + " " + address.dong,
            "latitude" : address.latitude,
            "longitude" : address.longitude
        }
        dongToSend.append(info)
    return myJsonResponse({"":dongToSend})

def getRecommendedPoint(request):
    memberId = request.headers["memberId"]
    recommendation = Recommendation.objects.select_related("memberTrend") \
        .select_related("dong1").select_related("dong2").select_related("dong3") \
        .select_related("dong4").select_related("dong5").get(memberTrend__member_id=memberId)

    labels = ["교통", "예산", "생활", "문화", "치안"]
    dongs = [recommendation.dong1, recommendation.dong2, recommendation.dong3, recommendation.dong4,
             recommendation.dong5]
    points = []
    for i, dong in enumerate(dongs, 1):
        address = Address.objects.get(areaCode=dong.areaCode)
        info = {
            "rank": i,
            "address": address.si + " " + address.gu + " " + address.dong,
             "transportation": dong.pointOfTransportation,
              "budget": dong.pointOfBudget,
              "life": dong.pointOfLife,
              "culture": dong.pointOfCulture,
              "safety": dong.pointOfSafety

        }
        points.append(info)
    data = {"labels" : labels, "status" : points}
    return myJsonResponse([data])

def getUserPoints(request):
    memberId = request.headers["memberId"]
    recommendation = Recommendation.objects.select_related("memberTrend").get(memberTrend__member_id=memberId)
    labels = ["교통", "예산", "생활", "문화", "치안"]
    userName = Member.objects.get(id=recommendation.memberTrend.member).name
    dataSet = {"transportation": recommendation.pointOfTransportation,
              "budget": recommendation.pointOfBudget,
              "life": recommendation.pointOfLife,
              "culture": recommendation.pointOfCulture,
              "safety": recommendation.pointOfSafety}
    data = {"labels" : labels, "username" : userName, "dataset" : dataSet}
    return myJsonResponse(data)

def getRoute(request):
    memberId = request.headers["memberId"]
    recommendation = Recommendation.objects.select_related("memberTrend") \
        .select_related("dong1").select_related("dong2").select_related("dong3") \
        .select_related("dong4").select_related("dong5").get(memberTrend__member_id__memberId=memberId)

    dongs = [recommendation.dong1, recommendation.dong2, recommendation.dong3, recommendation.dong4,
             recommendation.dong5]
    starts = FrequentPlace.objects.select_related("id").filter(id__memberId=memberId)
    url = "http://ws.bus.go.kr/api/rest/pathinfo/getPathInfoByBusNSub?serviceKey=jooMDUbQdPXfz9We%2BCA54k6P%2FwBFBviC%2FGnpipW0P%2FnnmgGfuTYjT%2BuEjxukjB78V42btkw3FkvLfhYHJd5Prg%3D%3D&"
          #"startX=126.890001872801&startY=37.5757542035555&endX=127.04249040816&endY=37.5804217059895&"
    data = []
    for i, dong in enumerate(dongs, 1):
        endX = dong.areaCode.longitude
        endY = dong.areaCode.latitude
        dongData = []
        for start in starts:
            startX = start.longitude
            startY = start.latitude
            http = httplib2.Http()
            finalurl = url + "startX=" + str(startX) + "&startY=" + str(startY) + "&endX=" + str(endX) + "&endY=" + str(endY)
            response, content = http.request(finalurl, "GET")
            content = content.decode("utf-8")
            xmlData = xmltodict.parse(content)
            jsonData = json.loads(json.dumps(xmlData, indent=4))
            print(jsonData)
            if jsonData["ServiceResult"]["msgHeader"]["headerCd"] == '0':
                items = jsonData["ServiceResult"]["msgBody"]["itemList"][0]["pathList"]
                route = ""
                routeDetail = []
                time = jsonData["ServiceResult"]["msgBody"]["itemList"][0]["time"]
                for item in items:
                    name = item["fname"]
                    number = item["routeNm"]
                    latitude = item["fy"]
                    longitude = item["fx"]
                    path = {"name" : name, "호선" : number, "위도" : latitude, "경도" : longitude}
                    routeDetail.append(path)
                    route += name + "(" + number + ")" + "->"
                route = route[0 : len(route) - 2]
                dataToSend = {"소요시간" : time, "경로" : route, "역정보" : routeDetail}
                dongData.append(dataToSend)
        data.append({"rank" : i, "route" : dongData})

    return myJsonResponse(data)