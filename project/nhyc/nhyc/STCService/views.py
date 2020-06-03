from collections import OrderedDict

from django.db.models.query import QuerySet, RawQuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework import permissions
import json
import pandas
import numpy as np
import httplib2

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
from .models import Average, Result_GuCnt, Result_GuDongCnt

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
# query = 'SELECT * FROM myapp_person WHERE last_name = %s' % gu

#####
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
def getCCTVCnt(request, gu=None):
    '''
    :param request: 
    :param gu: 
    :return: 서울시 내의 구들의 cctv 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 cctv 갯수를 리턴 (동이름으로 정렬된 데이터)
    '''

    resultString = []

    if gu is None:
        querySet = Result_GuCnt.objects.raw('''
            select gu, count(cctvId) as cnt
            from dataProcess_address A
            left outer join dataProcess_cctv B
            on A.areaCode = B.areaCode_id
            group by gu
            order by gu
            ''')
        print("querySet ::: ", querySet)
        for i in querySet:
            # print(i.gu, i.cnt)
            resultString.append(i.cnt)

    else:
        querySet = Result_GuDongCnt.objects.raw('''
            select gu, dong, count(cctvId) as cnt
            from dataProcess_address A
            left outer join dataProcess_cctv B
            on A.areaCode = B.areaCode_id
            where gu = '%s'
            group by dong
            order by dong
            ''' % gu)
        print(querySet)
        for i in querySet:
            # print(i.gu, i.dong, i.cnt)
            resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


@csrf_exempt
def getSecurityLightCnt(request, gu=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 보안등 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 보안등 갯수를 리턴 (동이름으로 정렬된 데이터)
    '''

    resultString = []

    if gu is None:
        querySet = Result_GuCnt.objects.raw('''
            select gu, count(lightId) as cnt
            from dataProcess_address A
            left outer join dataProcess_securitylight B
            on A.areaCode = B.areaCode_id
            group by gu
            order by gu
            ''')
        print("querySet ::: ", querySet)
        for i in querySet:
            # print(i.gu, i.cnt)
            resultString.append(i.cnt)

    else:
        querySet = Result_GuDongCnt.objects.raw('''
            select gu, dong, count(lightId) as cnt
            from dataprocess_address A
            left outer join dataProcess_securitylight B
            on A.areaCode = B.areaCode_id
            where gu = '%s'
            group by dong
            order by dong
            ''' % gu)
        print(querySet)
        for i in querySet:
            # print(i.gu, i.dong, i.cnt)
            resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


@csrf_exempt
def getPoliceOfficeCnt(request, gu=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 경찰시설 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 경찰시설 갯수를 리턴 (동이름으로 정렬된 데이터)
    '''

    resultString = []

    if gu is None:
        querySet = Result_GuCnt.objects.raw('''
            select gu, count(policeId) as cnt
            from dataProcess_address A
            left outer join dataProcess_policeoffice B
            on A.areaCode = B.areaCode_id
            group by gu
            order by gu
            ''')
        print("querySet ::: ", querySet)
        for i in querySet:
            # print(i.gu, i.cnt)
            resultString.append(i.cnt)

    else:
        querySet = Result_GuDongCnt.objects.raw('''
            select gu, dong, count(policeId) as cnt
            from dataProcess_address A
            left outer join dataProcess_policeoffice B
            on A.areaCode = B.areaCode_id
            where gu = '%s'
            group by dong
            order by dong
            ''' % gu)
        print(querySet)
        for i in querySet:
            # print(i.gu, i.dong, i.cnt)
            resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


########################## ↑↑↑↑↑↑↑↑ ############################


# ########################### ↓↓↓↓테스트 코드↓↓↓↓ ###########################
@csrf_exempt
def testQuery(request, gu, dong=None):
    '''
    :param request:
    :param gu: 원하는 구
    :param dong: 원하는 동 ()
    :return:
    '''
    if dong is None:
        resultXY = Gu.objects.filter(gu=gu)
    else:
        resultXY = Address.objects.filter(gu=gu, dong=dong)


@csrf_exempt
def testQuery2(request):  # 각 구별 월세, 보증금 데이터 읽기. 
    # 분석을 위해 pandas DataFrame 구조로 변환까지 완료

    querySet = Average.objects.raw('''
    SELECT gu , avg(rentalFee) as rentalFee, avg(deposit) as deposit 
    FROM dataProcess_address A 
    LEFT OUTER JOIN dataProcess_costrecord B 
    ON A.areaCode = left(B.houseNumber_id, 10) 
    GROUP BY gu
    ORDER BY gu
    ''')
    guList = []
    rentalFeeList = []
    depositList = []

    for i in querySet:
        guList.append(i.gu)
        rentalFeeList.append(i.rentalFee)
        depositList.append(i.deposit)

        print(i.gu, i.rentalFee, i.deposit)

    data = {'rentalFee': rentalFeeList,
            'deposit': depositList}

    df = pandas.DataFrame(data, index=guList)

    for i in df:
        print(df)

    return myJsonResponse(querySet)


# ########################### ↑↑↑↑테스트 코드↑↑↑↑ ###########################


# @csrf_exempt
# def testQuery(request, gu):  # areaCode입력 안 할 경우 전체 CCTV 검색
#     if request.method == 'GET':
#         resultArr = []  # HouseInfo들을 받아내는 최종 결과 배열
#
#         areaCodeArr = findGuAreaCodes(gu)
#
#         TOT = queryResult = HouseInfo.objects.filter(
#             areaCode=areaCodeArr[0])
#         for i in TOT:
#             resultArr.append(i)  # 그 결과값들을 resultArr에 붙여서 저장한다.
#
#         for currentAreaCode in areaCodeArr[1:]:
#             queryResult = HouseInfo.objects.filter(
#                 areaCode=currentAreaCode)  # 해당 areaCode로 검색된 결과(HouseInfo)를 testInfos에 저장
#             for i in queryResult:
#                 resultArr.append(i)  # 그 결과값들을 resultArr에 붙여서 저장한다.
#             TOT = TOT | queryResult
#
#     serializer = HouseInfoSerializer(TOT, many=True)
#
#     # print("TEST>>>>>>>>>>>>>>>>>>>>>>>>>>")
#     # print(finalResult.get(gu).length)
#     # print("TEST>>>>>>>>>>>>>>>>>>>>>>>>>>")
#     finalResult = JsonResponse({gu: serializer.data}, safe=False)  # <class 'django.http.response.JsonResponse'>
#
#     return finalResult


# @csrf_exempt
# def houseInfos(request, areaCode=None):  # 거래된 주택 정보 리딩 메소드
#     if request.method == 'GET':
#         if areaCode is not None:
#             query_set = HouseInfo.objects.filter(areaCode=areaCode)
#             # print(areaCode.__class__)
#         else:
#             query_set = HouseInfo.objects.all()  # <class 'django.db.models.query.QuerySet'>
#
#         serializer = HouseInfoSerializer(query_set, many=True)  # <class 'rest_framework.serializers.ListSerializer'>
#
#         iterator = serializer.data
#         number = 0
#         for i in iterator:  # i 자체가 OrderedDict형
#             number = number + 1
#             print("%d // " % number)
#             print(i)
#
#         print("serializer.data TYPE :: ")
#         print(iterator.__class__)
#         return JsonResponse(serializer.data, safe=False)  # << 이부분을 입맛에 따라 변경. 현재는 Json List 형식으로 리턴.
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = HouseInfoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)



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

def login(request):
    accessToken = request.headers["AccessToken"]
    baseUrl = "https://kapi.kakao.com/v2/user/me"
    authorization = "Bearer " + accessToken
    propertyKeys = ["properties.nickname", "kakao_account.age_range", "kakao_account.gender"]

    http = httplib2.Http()
    response, content = http.request(baseUrl, method="POST", headers={"Authorization": authorization},
                                     body={"property_keys": propertyKeys})
    content = content.decode("utf-8")
    jsonData = json.loads(content)
    print(jsonData)

    return HttpResponse(jsonData)
