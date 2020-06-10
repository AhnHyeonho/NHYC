import inspect
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
from .models import Average, Result_GuCnt, Result_GuDongCnt, TrendChartData

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
def getCCTVCnt(request, gu=None, dong=None):
    '''
    :param request: 
    :param gu: 
    :return: 서울시 내의 구들의 cctv 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 cctv 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 cctv 갯수를 리턴 (값 1개)
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
        if dong is None:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(cctvId) as cnt
                from dataProcess_address A
                left outer join dataProcess_cctv B
                on A.areaCode = B.areaCode_id
                where gu = '%s'
                group by dong
                order by dong
                ''' % gu)
            print("querySet ::: ", querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)
        else:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(cctvId) as cnt
                from dataProcess_address A
                left outer join dataProcess_cctv B
                on A.areaCode = B.areaCode_id
                where gu = '%s' AND dong='%s'
                group by dong
                order by dong
                ''' % (gu, dong))
            print("querySet ::: ", querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


@csrf_exempt
def getSecurityLightCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 보안등 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 보안등 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 보안등 갯수를 리턴 (값 1개)
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
        if dong is None:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(lightId) as cnt
                from dataProcess_address A
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
        else:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(lightId) as cnt
                from dataProcess_address A
                left outer join dataProcess_securitylight B
                on A.areaCode = B.areaCode_id
                where gu = '%s' AND dong='%s'
                group by dong
                order by dong
                ''' % (gu, dong))
            print("querySet ::: ", querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


def getPoliceOfficeCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 경찰시설 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 경찰시설 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 경찰시설 갯수를 리턴 (값 1개)
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
        if dong is None:
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
        else:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(policeId) as cnt
                from dataProcess_address A
                left outer join dataProcess_policeoffice B
                on A.areaCode = B.areaCode_id
                where gu = '%s' AND dong='%s'
                group by dong
                order by dong
                ''' % (gu, dong))
            print("querySet ::: ", querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


@csrf_exempt
def getRankingChartData(request, division, gu=None):
    '''
    :param request:
    :param division: rent면 월세기준, depo면 보증금 기준, rent-depo면 월세*12 + 보증금 기준
    :param gu: 있으면 해당 구의 차트 데이터 리딩
    :return: 정렬된 구, 월세, 보증금 리스트를 담은 JSON을 리턴
    '''

    if gu is None:
        print("서울시 기준 ::: ")
        queryString = '''
        SELECT gu , avg(rentalFee) as rentalFee, avg(deposit) as deposit
        FROM dataProcess_address A
        LEFT OUTER JOIN dataProcess_costrecord B
        ON A.areaCode = left(B.houseNumber_id, 10)
        GROUP BY gu
        ORDER BY gu
        '''

    else:
        print("%s 기준 ::: " % gu)
        queryString = '''
        SELECT dong as gu, avg(rentalFee) as rentalFee, avg(deposit) as deposit
        FROM dataProcess_address A
        LEFT OUTER JOIN dataProcess_costrecord B
        ON A.areaCode = left(B.houseNumber_id, 10)
        WHERE gu = '%s'
        GROUP BY dong
        ORDER BY dong
        ''' % gu

    querySet = Average.objects.raw(queryString)

    guList = []
    rentalFeeList = []
    depositList = []

    for i in querySet:
        guList.append(i.gu)
        rentalFeeList.append(i.rentalFee)
        depositList.append(i.deposit)

    data = {'gu': guList,
            'rentalFee': rentalFeeList,
            'deposit': depositList}
    rentalFeeRank = pandas.DataFrame(data)

    if division == 'rent':
        # 월세 기준
        print('월세 기준 >> :::')
        rentalFeeRank['rank'] = rentalFeeRank['rentalFee'].rank(method='min', ascending=True)  # 낮은 가격순으로 순위 저장
        rentalFeeRank.sort_values(by=['rentalFee'], axis=0, inplace=True, ascending=True)  # 낮은 순위부터 정렬
    elif division == 'depo':
        # 보증금 기준
        print('보증금 기준 >> :::')
        rentalFeeRank['rank'] = rentalFeeRank['deposit'].rank(method='min', ascending=True)  # 낮은 가격순으로 순위 저장
        rentalFeeRank.sort_values(by=['deposit'], axis=0, inplace=True, ascending=True)  # 낮은 순위부터 정렬
    elif division == 'rent-depo':
        # 월세 1년치(12개월) + 보증금 기준
        print('월세 1년치(12개월) + 보증금 기준 >> :::')
        rentalFeeRank['year-rent'] = rentalFeeRank['rentalFee'] * 12  # 12개월치 월세
        rentalFeeRank['rent-deposit'] = rentalFeeRank['year-rent'] + rentalFeeRank['deposit']  # 12개월치 월세 + 보증금
        rentalFeeRank['rank'] = rentalFeeRank['rent-deposit'].rank(method='min', ascending=True)  # 낮은 가격순으로 순위 저장
        rentalFeeRank.sort_values(by=['deposit'], axis=0, inplace=True, ascending=True)  # 낮은 순위부터 정렬
    else:
        return JsonResponse(data.errors, status=400)

    print(rentalFeeRank)

    guList = rentalFeeRank['gu'].tolist()
    rentalFeeList = rentalFeeRank['rentalFee'].tolist()
    depositList = rentalFeeRank['deposit'].tolist()
    rentalFeeList = list(map(str, rentalFeeList))  # Decimal 형태의 index들을 단순 string으로 변환
    depositList = list(map(str, depositList))  # Decimal 형태의 index들을 단순 string으로 변환

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
def getPharmacyCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 약국 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 약국 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 약국 갯수를 리턴 (값 1개)
    '''
    resultString = []

    if gu is None:
        querySet = Result_GuCnt.objects.raw('''
            select gu, count(pharmacyId) as cnt
            from dataProcess_address A
            left outer join dataProcess_pharmacy B
            on A.areaCode = B.areaCode_id
            group by gu
            order by gu
            ''')
        print("querySet ::: ", querySet)
        for i in querySet:
            # print(i.gu, i.cnt)
            resultString.append(i.cnt)

    else:
        if dong is None:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(pharmacyId) as cnt
                from dataProcess_address A
                left outer join dataProcess_pharmacy B
                on A.areaCode = B.areaCode_id
                where gu = '%s'
                group by dong
                order by dong
                ''' % gu)
            print(querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)
        else:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(pharmacyId) as cnt
                from dataProcess_address A
                left outer join dataProcess_pharmacy B
                on A.areaCode = B.areaCode_id
                where gu = '%s' AND dong='%s'
                group by dong
                order by dong
                ''' % (gu, dong))
            print("querySet ::: ", querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


@csrf_exempt
def getMarketCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 전통시장 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 전통시장 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 전통시장 갯수를 리턴 (값 1개)
    '''
    resultString = []

    if gu is None:
        querySet = Result_GuCnt.objects.raw('''
            select gu, count(marketId) as cnt
            from dataProcess_address A
            left outer join dataProcess_market B
            on A.areaCode = B.areaCode_id
            group by gu
            order by gu
            ''')
        print("querySet ::: ", querySet)
        for i in querySet:
            # print(i.gu, i.cnt)
            resultString.append(i.cnt)

    else:
        if dong is None:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(marketId) as cnt
                from dataProcess_address A
                left outer join dataProcess_market B
                on A.areaCode = B.areaCode_id
                where gu = '%s'
                group by dong
                order by dong
                ''' % gu)
            print(querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)
        else:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(marketId) as cnt
                from dataProcess_address A
                left outer join dataProcess_market B
                on A.areaCode = B.areaCode_id
                where gu = '%s' AND dong='%s'
                group by dong
                order by dong
                ''' % (gu, dong))
            print("querySet ::: ", querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


@csrf_exempt
def getParkCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 공원 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 공원 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 공원 갯수를 리턴 (값 1개)
    '''
    resultString = []

    if gu is None:
        querySet = Result_GuCnt.objects.raw('''
            select gu, count(parkId) as cnt
            from dataProcess_address A
            left outer join dataProcess_park B
            on A.areaCode = B.areaCode_id
            group by gu
            order by gu
            ''')
        print("querySet ::: ", querySet)
        for i in querySet:
            # print(i.gu, i.cnt)
            resultString.append(i.cnt)

    else:
        if dong is None:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(parkId) as cnt
                from dataProcess_address A
                left outer join dataProcess_park B
                on A.areaCode = B.areaCode_id
                where gu = '%s'
                group by dong
                order by dong
                ''' % gu)
            print(querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)
        else:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(parkId) as cnt
                from dataProcess_address A
                left outer join dataProcess_park B
                on A.areaCode = B.areaCode_id
                where gu = '%s' AND dong='%s'
                group by dong
                order by dong
                ''' % (gu, dong))
            print("querySet ::: ", querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


@csrf_exempt
def getGymCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 공공체육시설 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 공공체육시설 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 공공체육시설 갯수를 리턴 (값 1개)
    '''
    resultString = []

    if gu is None:
        querySet = Result_GuCnt.objects.raw('''
            select gu, count(gymId) as cnt
            from dataProcess_address A
            left outer join dataProcess_gym B
            on A.areaCode = B.areaCode_id
            group by gu
            order by gu
            ''')
        print("querySet ::: ", querySet)
        for i in querySet:
            # print(i.gu, i.cnt)
            resultString.append(i.cnt)

    else:
        if dong is None:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(gymId) as cnt
                from dataProcess_address A
                left outer join dataProcess_gym B
                on A.areaCode = B.areaCode_id
                where gu = '%s'
                group by dong
                order by dong
                ''' % gu)
            print(querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)
        else:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(gymId) as cnt
                from dataProcess_address A
                left outer join dataProcess_gym B
                on A.areaCode = B.areaCode_id
                where gu = '%s' AND dong='%s'
                group by dong
                order by dong
                ''' % (gu, dong))
            print("querySet ::: ", querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


@csrf_exempt
def getConcertHallCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 공연장 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 공연장 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 공연장 갯수를 리턴 (값 1개)
    '''
    resultString = []

    if gu is None:
        querySet = Result_GuCnt.objects.raw('''
            select gu, count(concertHallId) as cnt
            from dataProcess_address A
            left outer join dataProcess_concerthall B
            on A.areaCode = B.areaCode_id
            group by gu
            order by gu
            ''')
        print("querySet ::: ", querySet)
        for i in querySet:
            # print(i.gu, i.cnt)
            resultString.append(i.cnt)

    else:
        if dong is None:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(concertHallId) as cnt
                from dataProcess_address A
                left outer join dataProcess_concerthall B
                on A.areaCode = B.areaCode_id
                where gu = '%s'
                group by dong
                order by dong
                ''' % gu)
            print(querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)
        else:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(concertHallId) as cnt
                from dataProcess_address A
                left outer join dataProcess_concerthall B
                on A.areaCode = B.areaCode_id
                where gu = '%s' AND dong='%s'
                group by dong
                order by dong
                ''' % (gu, dong))
            print("querySet ::: ", querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


@csrf_exempt
def getLibraryCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 도서관 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 도서관 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 도서관 갯수를 리턴 (값 1개)
    '''
    resultString = []

    if gu is None:
        querySet = Result_GuCnt.objects.raw('''
            select gu, count(libraryId) as cnt
            from dataProcess_address A
            left outer join dataProcess_library B
            on A.areaCode = B.areaCode_id
            group by gu
            order by gu
            ''')
        print("querySet ::: ", querySet)
        for i in querySet:
            # print(i.gu, i.cnt)
            resultString.append(i.cnt)

    else:
        if dong is None:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(libraryId) as cnt
                from dataProcess_address A
                left outer join dataProcess_library B
                on A.areaCode = B.areaCode_id
                where gu = '%s'
                group by dong
                order by dong
                ''' % gu)
            print(querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)
        else:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(libraryId) as cnt
                from dataProcess_address A
                left outer join dataProcess_library B
                on A.areaCode = B.areaCode_id
                where gu = '%s' AND dong='%s'
                group by dong
                order by dong
                ''' % (gu, dong))
            print("querySet ::: ", querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


@csrf_exempt
def getCulturalFacilityCnt(request, gu=None, dong=None):
    '''
    :param request:
    :param gu:
    :return: 서울시 내의 구들의 박물관/미술관 갯수를 리턴. (구이름으로 정렬된 데이터)
             만약 gu값이 입려 되어있다면 해당 구 내의 동들의 박물관/미술관 갯수를 리턴 (동이름으로 정렬된 데이터)
             만약 dong값까지 입력되었다면 해당 동의 박물관/미술관 갯수를 리턴 (값 1개)
    '''
    resultString = []

    if gu is None:
        querySet = Result_GuCnt.objects.raw('''
            select gu, count(culturalFacilityId) as cnt
            from dataProcess_address A
            left outer join dataProcess_culturalfacility B
            on A.areaCode = B.areaCode_id
            group by gu
            order by gu
            ''')
        print("querySet ::: ", querySet)
        for i in querySet:
            # print(i.gu, i.cnt)
            resultString.append(i.cnt)

    else:
        if dong is None:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(culturalFacilityId) as cnt
                from dataProcess_address A
                left outer join dataProcess_culturalfacility B
                on A.areaCode = B.areaCode_id
                where gu = '%s'
                group by dong
                order by dong
                ''' % gu)
            print(querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)
        else:
            querySet = Result_GuDongCnt.objects.raw('''
                select gu, dong, count(culturalFacilityId) as cnt
                from dataProcess_address A
                left outer join dataProcess_culturalfacility B
                on A.areaCode = B.areaCode_id
                where gu = '%s' AND dong='%s'
                group by dong
                order by dong
                ''' % (gu, dong))
            print("querySet ::: ", querySet)
            for i in querySet:
                # print(i.gu, i.dong, i.cnt)
                resultString.append(i.cnt)

    print(resultString)
    return myJsonResponse(resultString)


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
            addressInfo.save()
            print(addressInfo)
        else:
            print(i.gu, '데이터 존재!! 기존 데이터 수정::>>')
            addressInfo.si = i.si
            addressInfo.gu = i.gu
            addressInfo.dong = i.dong
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
        SELECT gu, dong, avg(rentalFee) as rentalFee, avg(deposit) as deposit, count(houseNumber_id) as cnt
        FROM dataProcess_address A
        LEFT OUTER JOIN dataProcess_costrecord B
        ON A.areaCode = left(B.houseNumber_id, 10)
        GROUP BY dong
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


# dummyData ↓↓↓
@csrf_exempt
def getDummyDataForDH(request):
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

    return HttpResponse(dummyData)


# dummyData ↑↑↑

########################## ↑↑↑↑↑↑↑↑ ############################


# ########################### ↓↓↓↓테스트 코드↓↓↓↓ ###########################
@csrf_exempt
def testQuery(request):
    queryString = '''
        SELECT gu, dong, avg(rentalFee) as rentalFee, avg(deposit) as deposit
        FROM dataProcess_address A
        LEFT OUTER JOIN dataProcess_costrecord B
        ON A.areaCode = left(B.houseNumber_id, 10)
        GROUP BY dong
        ORDER BY dong
    '''
    querySet = Average.objects.raw(queryString)  # 각 동별 평균 월세, 보증금 계산

    print('querySet:>> ', querySet)

    for i in querySet:
        addressInfo, created = AddressInfo.objects.get_or_create(gu=i.gu, dong=i.dong)
        addressInfo.avgDeposit = i.deposit
        addressInfo.avgRentalFee = i.rentalFee
        addressInfo.save()
        print(addressInfo)

    print('addingAvgAddressInfo done')
    return HttpResponse('addingAvgAddressInfo done')


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
#             'deposit': depositList}
#
#     df = pandas.DataFrame(data, index=guList)
#
#     for i in df:
#         print(df)
#
#     return myJsonResponse(querySet)


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

            memberInfo = MemberInfo(member=member, gender=None, age_range=None, money=None)

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

def join(request):
    id = request.headers["id"]
    email = request.headers["email"]
    password = request.headers["password"]
    name = request.headers["name"]
    member = Member(id=id, email=email, password=password, name=name)
    member.save()

    memberInfo = MemberInfo(member=member, gender=None, age_range=None, money=None)
    if "gender" in request.headers:
        gender = request.headers["gender"]
        setattr(memberInfo, "gender", gender)

    if "age_range" in request.headers:
        age_range = request.headers["age_range"]
        setattr(memberInfo, "age_range", age_range)

    if "money" in request.headers:
        money = request.headers["money"]
        setattr(memberInfo, "money", money)

    memberInfo.save()

    return HttpResponse("join")

def login(request):
    id = request.headers["id"]
    password = request.headers["password"]

    if Member.objects.filter(id=id, password=password):
        return HttpResponse("login success")
    else:
        return HttpResponse("login fail")