import httplib2
import json
import nhyc.settings as settings
import os
import pandas, numpy
import re
import urllib.request
import xlrd
from datetime import date, datetime
from django.http import HttpResponse
from django.shortcuts import render
from urllib.parse import quote

from .models import Address
from .models import CCTV
from .models import CostRecord
from .models import FrequentPlace
from .models import HouseInfo
from .models import Member
from .models import MemberInfo
from .models import PoliceOffice
from .models import SecurityLight

naverClientId = "tw8yh1kfp6"
naverClientPasswd = "Djx3jNQ1bbXODDxgZM9GS8XL391dPXB2VyxsbO2E"
naverGeocodeURL = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
naverReverseGeocodeURL = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"

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


def getHouseInfo(request, num):
    url = "http://openapi.seoul.go.kr:8088/545149464a73696c39326f47667644/json/houseRentPriceInfo/"
    start = num
    end = num + 999

    while (True):
        http = httplib2.Http()
        finalurl = url + str(start) + "/" + str(end)
        response, content = http.request(finalurl, "GET")
        content = content.decode("utf-8")
        jsonData = json.loads(content)

        data = jsonData["houseRentPriceInfo"]["row"]

        for info in data:
            if (info["HOUSE_GBN_NM"] == "다세대/연립" and "월세" in info["RENT_CASE_NM"]):
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
                    if geocode["meta"]["count"] != 0:
                        latitude = geocode["addresses"][0]["y"]
                        longitude = geocode["addresses"][0]["x"]
                        houseInfo = HouseInfo(houseNumber=houseNumber, latitude=latitude, longitude=longitude,
                                              pyeong=pyeong, houseName=houseName, areaCode=areaCode)
                        houseInfo.save()
                    else:
                        print(query)
                if (HouseInfo.objects.filter(houseNumber=info["LAND_CD"]).count() == 1):
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

def getCCTV(request):
    cctvPath = os.path.join(settings.BASE_DIR, "dataProcess", "CCTV")
    fileList = os.listdir(cctvPath)

    for fileName in fileList:
        csv = pandas.read_csv(os.path.join(cctvPath, fileName), encoding="CP949")

        for i in csv.index:
            gu = ""
            dong = ""

            if pandas.notnull(csv.at[i, "위도"]) and pandas.notnull(csv.at[i, "경도"]):
                latitude = csv.at[i, "위도"]
                longitude = csv.at[i, "경도"]

                if(CCTV.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
                    naverURL = naverReverseGeocodeURL + "?coords=" + str(longitude) + "," + str(
                        latitude) + "&orders=legalcode&output=json"
                    https = urllib.request.Request(naverURL)
                    https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                    https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                    response = urllib.request.urlopen(https)
                    content = response.read()
                    content = content.decode("utf-8")

                    addressData = json.loads(content)
                    print(addressData)

                    if addressData["status"]["name"] == "ok":
                        region = addressData["results"][0]["region"]
                        gu = region["area2"]["name"]
                        dong = region["area3"]["name"]
                        print(gu + " " + dong)

            else:
                if pandas.notnull(csv.at[i, "소재지도로명주소"]):
                    address = csv.at[i, "소재지도로명주소"]
                else:
                    address = csv.at[i, "소재지지번주소"]

                print(address)

                naverURL = naverGeocodeURL + "?query=" + quote(address)
                https = urllib.request.Request(naverURL)
                https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                response = urllib.request.urlopen(https)
                content = response.read()
                content = content.decode("utf-8")

                geocode = json.loads(content)
                if geocode["meta"]["count"] != 0:
                    latitude = geocode["addresses"][0]["y"]
                    longitude = geocode["addresses"][0]["x"]
                    addressSplit = geocode["addresses"][0]["jibunAddress"].split()
                    gu = addressSplit[1]
                    dong = addressSplit[2]

            if Address.objects.filter(gu=gu, dong=dong).count == 1:
                areaCode = Address.objects.get(gu=gu, dong=dong)
                if CCTV.objects.filter(areaCode=areaCode.areaCode):
                    cctv = CCTV(latitude=latitude, longitude=longitude, areaCode=areaCode)
                    cctv.save()

    return HttpResponse(csv)

def getSecurityLight(request):
    cctvPath = os.path.join(settings.BASE_DIR, "dataProcess", "보안등")
    fileList = os.listdir(cctvPath)

    for fileName in fileList:
        csv = pandas.read_csv(os.path.join(cctvPath, fileName), encoding="CP949")
        for i in csv.index:
            gu = ""
            dong = ""
            if pandas.notnull(csv.at[i, "위도"]) and pandas.notnull(csv.at[i, "경도"]):
                latitude = csv.at[i, "위도"]
                longitude = csv.at[i, "경도"]

                if (SecurityLight.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
                    naverURL = naverReverseGeocodeURL + "?coords=" + str(longitude) + "," + str(
                        latitude) + "&orders=legalcode&output=json"
                    https = urllib.request.Request(naverURL)
                    https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                    https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                    response = urllib.request.urlopen(https)
                    content = response.read()
                    content = content.decode("utf-8")

                    addressData = json.loads(content)
                    print(addressData)

                    if addressData["status"]["name"] == "ok":
                        region = addressData["results"][0]["region"]
                        gu = region["area2"]["name"]
                        dong = region["area3"]["name"]
                        print(gu + " " + dong)

            else:
                if pandas.notnull(csv.at[i, "소재지도로명주소"]):
                    address = csv.at[i, "소재지도로명주소"]
                else:
                    address = csv.at[i, "소재지지번주소"]

                print(address)

                naverURL = naverGeocodeURL + "?query=" + quote(address)
                https = urllib.request.Request(naverURL)
                https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                response = urllib.request.urlopen(https)
                content = response.read()
                content = content.decode("utf-8")

                geocode = json.loads(content)
                if geocode["meta"]["count"] != 0:
                    latitude = geocode["addresses"][0]["y"]
                    longitude = geocode["addresses"][0]["x"]
                    addressSplit = geocode["addresses"][0]["jibunAddress"].split()
                    gu = addressSplit[1]
                    dong = addressSplit[2]
            if Address.objects.filter(gu=gu, dong=dong).count == 1:
                areaCode = Address.objects.get(gu=gu, dong=dong)
                if SecurityLight.objects.filter(areaCode = areaCode.areaCode):
                    securityLight = SecurityLight(latitude=latitude, longitude=longitude, areaCode=areaCode)
                    securityLight.save()

    return HttpResponse(csv)

def getPoliceOffice(request):
    csv = pandas.read_csv(os.path.join(settings.BASE_DIR, "dataProcess/경찰관서위치_20200409.csv"), encoding = "CP949")
    csv = csv.dropna()
    csv = csv[csv["청"].str.contains("서울")]

    for i in csv.index:
        latitude = csv.at[i, "Y좌표"]
        longitude = csv.at[i, "X좌표"]

        if (PoliceOffice.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
            naverURL = naverReverseGeocodeURL + "?coords=" + str(longitude) + "," + str(latitude) + "&orders=legalcode&output=json"
            https = urllib.request.Request(naverURL)
            https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
            https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
            response = urllib.request.urlopen(https)
            content = response.read()
            content = content.decode("utf-8")

            addressData = json.loads(content)
            print(addressData)

            if addressData["status"]["name"] == "ok":
                region = addressData["results"][0]["region"]
                gu = region["area2"]["name"]
                dong = region["area3"]["name"]
                print(gu + " " + dong)
                areaCode = Address.objects.get(gu=gu, dong=dong)
                policeOfficeName = csv.get_value(i, "지구대파출소")
                policeOffice = PoliceOffice(latitude=latitude, longitude=longitude, policeOfficeName=policeOfficeName, areaCode=areaCode)
                policeOffice.save()

    return HttpResponse(csv)