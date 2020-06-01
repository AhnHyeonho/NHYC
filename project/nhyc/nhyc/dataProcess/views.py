from django.http import HttpResponse
from django.shortcuts import render
import json, httplib2, urllib.request
from urllib.parse import quote
import pandas
import os
import nhyc.settings as settings
from datetime import date, datetime

from .models import Member
from .models import Address
from .models import MemberInfo
from .models import FrequentPlace
from .models import HouseInfo
from .models import CostRecord
from .models import CCTV
from .models import SecurityLight
from .models import PoliceOffice

naverClientId = "tw8yh1kfp6"
naverClientPasswd = "Djx3jNQ1bbXODDxgZM9GS8XL391dPXB2VyxsbO2E"
naverGeocodeURL = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"


def getAddress(reqeust):
    data = pandas.read_excel(os.path.join(settings.BASE_DIR, "dataProcess/법정동코드 전체자료.xlsx"))

    data["시"] = data["법정동명"].str.split(" ").str[0]
    data["구"] = data["법정동명"].str.split(" ").str[1]
    data["동"] = data["법정동명"].str.split(" ").str[2]

    data = data.dropna()
    data = data[(data["폐지여부"] == "존재") & (data["시"] == "서울특별시")]
    data = data.reset_index(drop=True, inplace=False)

    for i in data.index:
        areaCode = data.get_value(i, "법정동코드")# <<<---여기인거 같어
        si = data.get_value(i, "시")
        gu = data.get_value(i, "구")
        dong = data.get_value(i, "동")
        address = Address(areaCode=areaCode, si=si, gu=gu, dong=dong)
        address.save()

    return HttpResponse()


def getHouseInfo(request):
    url = "http://openapi.seoul.go.kr:8088/545149464a73696c39326f47667644/json/houseRentPriceInfo/"
    start = 1
    end = 1000

    while (True):

        http = httplib2.Http()
        finalurl = url + str(start) + "/" + str(end)
        response, content = http.request(finalurl, "GET")
        content = content.decode("utf-8")
        jsonData = json.loads(content)

        data = jsonData["houseRentPriceInfo"]["row"]

        for info in data:
            if (info["HOUSE_GBN_NM"] == "다세대/연립" and info["RENT_CASE_NM"] == "월세"):
                if (HouseInfo.objects.filter(houseNumber=info["LAND_CD"]).count() == 0):
                    houseNumber = info["LAND_CD"]
                    pyeong = float(info["RENT_AREA"]) * 0.3025
                    houseName = info["BLDG_NM"]
                    areaCode = Address.objects.get(gu=info["SGG_NM"], dong=info["BJDONG_NM"])
                    query = info["SGG_NM"] + " " + info["BJDONG_NM"] + " " + str(int(info["BOBN"])) + "-" + str(
                        int(info["BUBN"]))
                    naverURL = naverGeocodeURL + "?query=" + quote(query)
                    https = urllib.request.Request(naverURL)
                    https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                    https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                    response = urllib.request.urlopen(https)
                    content = response.read()
                    content = content.decode("utf-8")

                    geocode = json.loads(content)
                    latitude = geocode["addresses"][0]["y"]
                    longitude = geocode["addresses"][0]["x"]
                    houseInfo = HouseInfo(houseNumber=houseNumber, latitude=latitude, longitude=longitude,
                                          pyeong=pyeong, houseName=houseName, areaCode=areaCode)
                    houseInfo.save()

                houseNumber = HouseInfo.objects.get(houseNumber=info["LAND_CD"])
                day = datetime.strptime(info["CNTRCT_DE"], "%Y%m%d").date()
                if (CostRecord.objects.filter(houseNumber=houseNumber, day=day).count() == 0):
                    costRecordId = houseNumber.houseNumber + str(
                        CostRecord.objects.filter(houseNumber=houseNumber).count() + 1)
                    rentalFee = info["RENT_FEE"]
                    deposit = info["RENT_GTN"]
                    costRecord = CostRecord(costRecordId=costRecordId, houseNumber=houseNumber,
                                            day=day, rentalFee=rentalFee, deposit=deposit)
                    costRecord.save()

        if len(data) != 1000: break;
        print(start)
        start = end + 1
        end = start + 999

    return HttpResponse(jsonData)