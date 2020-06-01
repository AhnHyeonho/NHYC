from collections import OrderedDict

from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework import permissions
import json
import numpy as np

from dataProcess.models import Member
from .serializers import MemberSerializer
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
from .models import Average

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


##### 메모장..
# for gu, gu_areaCode in seoulGu.items():  # Dict형 key, value읽어오기

#####


# ########################### ↓↓↓↓테스트 코드↓↓↓↓ ###########################
# @csrf_exempt
# def testQuery(request):  # areaCode입력 안 할 경우 전체 CCTV 검색
#     name_map = {'B.gu': 'gu', 'avg(A.rentalFee)': 'rentalFee', 'avg(A.deposit)': 'deposit'}
#     for i in Average.objects.raw('''
#     SELECT B.gu , avg(A.rentalFee), avg(A.deposit)
# FROM dataprocess_costrecord A
# LEFT JOIN dataprocess_address B
# ON left(A.houseNumber_id, 10) = B.areaCode
# GROUP BY left(A.houseNumber_id ,5)
#     '''):
#         print(i)


# ########################### ↑↑↑↑테스트 코드↑↑↑↑ ###########################

@csrf_exempt
def Member(request, id):
    if request.method == 'GET':
        if id is not None:
            query_set = Member.objects.filter(id=id)
        else:
            query_set = Member.objects.all()

        serializer = MemberSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)  # << 이부분을 입맛에 따라 변경. 현재는 Json List 형식으로 리턴.

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MemberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def testQuery(request, gu):  # areaCode입력 안 할 경우 전체 CCTV 검색
    if request.method == 'GET':
        resultArr = []  # HouseInfo들을 받아내는 최종 결과 배열

        areaCodeArr = findGuAreaCodes(gu)

        TOT = queryResult = HouseInfo.objects.filter(
            areaCode=areaCodeArr[0])
        for i in TOT:
            resultArr.append(i)  # 그 결과값들을 resultArr에 붙여서 저장한다.

        for currentAreaCode in areaCodeArr[1:]:
            queryResult = HouseInfo.objects.filter(
                areaCode=currentAreaCode)  # 해당 areaCode로 검색된 결과(HouseInfo)를 testInfos에 저장
            for i in queryResult:
                resultArr.append(i)  # 그 결과값들을 resultArr에 붙여서 저장한다.
            TOT = TOT | queryResult

    serializer = HouseInfoSerializer(TOT, many=True)

    # print("TEST>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # print(finalResult.get(gu).length)
    # print("TEST>>>>>>>>>>>>>>>>>>>>>>>>>>")
    finalResult = JsonResponse({gu: serializer.data}, safe=False)  # <class 'django.http.response.JsonResponse'>

    return finalResult


@csrf_exempt
def houseInfos(request, areaCode=None):  # 거래된 주택 정보 리딩 메소드
    if request.method == 'GET':
        if areaCode is not None:
            query_set = HouseInfo.objects.filter(areaCode=areaCode)
            # print(areaCode.__class__)
        else:
            query_set = HouseInfo.objects.all()  # <class 'django.db.models.query.QuerySet'>

        serializer = HouseInfoSerializer(query_set, many=True)  # <class 'rest_framework.serializers.ListSerializer'>

        iterator = serializer.data
        number = 0
        for i in iterator:  # i 자체가 OrderedDict형
            number = number + 1
            print("%d // " % number)
            print(i)

        print("serializer.data TYPE :: ")
        print(iterator.__class__)
        return JsonResponse(serializer.data, safe=False)  # << 이부분을 입맛에 따라 변경. 현재는 Json List 형식으로 리턴.

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HouseInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def getCCTVs(request, areaCode_id=None):  # areaCode입력 안 할 경우 전체 CCTV 검색
    if request.method == 'GET':
        if areaCode_id is not None:
            query_set = CCTV.objects.filter(areaCode_id=areaCode_id)
        else:
            query_set = CCTV.objects.all()
        serializer = CCTVSerializer(query_set, many=True)
        return serializer.data  # 해당 조건 쿼리셋으로 받아온 CCTV 데이터 (JSON형식) -> tuple


@csrf_exempt
def getSecurityLights(request, areaCode_id=None):  # areaCode입력 안 할 경우 전체 보안등 검색
    if request.method == 'GET':
        if areaCode_id is not None:
            query_set = SecurityLight.objects.filter(areaCode_id=areaCode_id)
        else:
            query_set = SecurityLight.objects.all()
        serializer = SecurityLightSerializer(query_set, many=True)
        return serializer.data  # 해당 조건 쿼리셋으로 받아온 보안등 데이터 (JSON형식) -> tuple


@csrf_exempt
def getPoliceOffices(request, areaCode_id=None):  # areaCode입력 안 할 경우 경찰시설 검색
    if request.method == 'GET':
        if areaCode_id is not None:
            query_set = PoliceOffice.objects.filter(areaCode_id=areaCode_id)
        else:
            query_set = PoliceOffice.objects.all()
        serializer = PoliceOfficeSerializer(query_set, many=True)
        return serializer.data  # 해당 조건 쿼리셋으로 받아온 경찰시설 데이터 (JSON형식) -> tuple


########################## ↓↓↓↓↓↓↓↓ ############################
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


@csrf_exempt
def getGu(request):
    # 구 이름만 배열로..
    returnString = []
    for i in seoulGu:
        returnString.append(i)
        print(i)

    return JsonResponse(returnString, safe=False)


########################## ↑↑↑↑↑↑↑↑ ############################


@csrf_exempt
def loadSeoulSiData():
    resultCCTVArr = []

    for currentGu in seoulGu:  # 종로구 areaCode전체 하나하나 돌면서
        getCCTVInfosByGu



######################### Login ####################################

'''def login(request):
    accessToken = request.headers["AccessToken"]
    baseUrl = "kapi.kakao.com"'''

