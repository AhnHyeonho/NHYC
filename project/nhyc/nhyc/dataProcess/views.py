from django.http import HttpResponse
from django.shortcuts import render
import json, httplib2, urllib.request
from urllib.parse import quote
import pandas, xlrd
import os
import nhyc.settings as settings
from datetime import date, datetime
import re

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

def getCCTV(request):
    data = open(os.path.join(settings.BASE_DIR, "dataProcess/전국CCTV표준데이터.json"), encoding="utf-8")
    jsonData = json.load(data)

    fields = jsonData["fields"]
    records = jsonData["records"]

    for record in records:
        address = ""
        if fields[1]["id"] in record:
            address = record[fields[1]["id"]]
        else:
            address = record[fields[2]["id"]]
            p = re.compile("([^0-9]+)[0-9]+[-][0-9]+")
            address = p.sub("\g<1>", address)

        if "서울특별시" in address:
            latitude = record[fields[10]["id"]]
            longitude = record[fields[11]["id"]]

            if(CCTV.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
                url = "http://api.vworld.kr/req/search"
                key = "615BD760-6D49-3D5E-894A-B787D1F5D0FB"

                url = url + "?request=search&type=address&category=road&size=1&key=" + key + "&query=" + quote(
                    address)
                '''if fields[1]["id"] in record:
                    
                else:
                    url = url + "?request=search&type=address&category=parcel&size=1&key=" + key + "&query=" + quote(
                        address)'''

                http = urllib.request.Request(url)
                response = urllib.request.urlopen(http)
                content = response.read()
                content = content.decode("utf-8")
                jsonData = json.loads(content)
                resultCode = jsonData["response"]["status"]
                if resultCode == "OK":
                    code = jsonData["response"]["result"]["items"][0]["id"]
                    code = code[0:10]

                    areaCode = Address.objects.get(areaCode = code)
                    print(areaCode.gu + " " + areaCode.dong)
                    cctv = CCTV(latitude=latitude, longitude=longitude, areaCode=areaCode)
                    cctv.save()
                else:
                    print(address)

    return HttpResponse(fields)

def getSecurityLight(request):
    data = open(os.path.join(settings.BASE_DIR, "dataProcess/전국보안등정보표준데이터.json"), encoding="utf-8")
    jsonData = json.load(data)

    fields = jsonData["fields"]
    records = jsonData["records"]

    for record in records:
        address = ""
        if fields[2]["id"] in record:
            address = record[fields[2]["id"]]
        else:
            address = record[fields[3]["id"]]
            p = re.compile("([^0-9]+)[0-9]+[-][0-9]+")
            address = p.sub("\g<1>", address)

        if "서울특별시" in address:
            if fields[4]["id"] in record and fields[5]["id"] in record:
                latitude = record[fields[4]["id"]]
                longitude = record[fields[5]["id"]]

                if (SecurityLight.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
                    url = "http://api.vworld.kr/req/search"
                    key = "615BD760-6D49-3D5E-894A-B787D1F5D0FB"

                    url = url + "?request=search&type=address&category=road&size=1&key=" + key + "&query=" + quote(
                        address)
                    http = urllib.request.Request(url)
                    response = urllib.request.urlopen(http)
                    content = response.read()
                    content = content.decode("utf-8")
                    jsonData = json.loads(content)
                    resultCode = jsonData["response"]["status"]
                    if resultCode == "OK":
                        code = jsonData["response"]["result"]["items"][0]["id"]
                        code = code[0:10]

                        areaCode = Address.objects.get(areaCode=code)
                        print(areaCode.gu + " " + areaCode.dong)
                        securityLight = SecurityLight(latitude=latitude, longitude=longitude, areaCode=areaCode)
                        securityLight.save()
                    else:
                        print(address)

    return HttpResponse(fields)

def getPoliceOffice(request):
    csv = pandas.read_csv(os.path.join(settings.BASE_DIR, "dataProcess/경찰관서위치_20200409.csv"), encoding = "CP949")
    csv = csv.dropna()
    csv = csv[csv["청"].str.contains("서울")]

    for i in csv.index:
        address = csv.get_value(i, "주소")
        latitude = csv.get_value(i, "Y좌표")
        longitude = csv.get_value(i, "X좌표")
        policeOfficeName = csv.get_value(i, "지구대파출소")
        #print(address + " " + str(latitude) + " " + str(longitude) + " " + policeOfficeName)

        if (PoliceOffice.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
            baseUrl = "http://api.vworld.kr/req/search"
            key = "615BD760-6D49-3D5E-894A-B787D1F5D0FB"

            url = baseUrl + "?request=search&type=place&size=1&key=" + key + "&query=" + quote(
                policeOfficeName)
            http = urllib.request.Request(url)
            response = urllib.request.urlopen(http)
            content = response.read()
            content = content.decode("utf-8")
            jsonData = json.loads(content)
            print(jsonData)

            url = baseUrl + "?request=search&type=address&category=road&size=1&key=" + key + "&query=" + quote(
                jsonData["response"]["result"]["items"][0]["address"]["road"])
            print(url)
            http = urllib.request.Request(url)
            response = urllib.request.urlopen(http)
            content = response.read()
            content = content.decode("utf-8")
            jsonData = json.loads(content)

            resultCode = jsonData["response"]["status"]
            print(jsonData)
            if resultCode == "OK":
                code = jsonData["response"]["result"]["items"][0]["id"]
                code = code[0:10]
                print(code)
                if Address.objects.filter(areaCode=code).count() == 1:
                    areaCode = Address.objects.get(areaCode=code)
                    print(areaCode.gu + " " + areaCode.dong)
                    policeOffice = PoliceOffice(latitude=latitude, longitude=longitude, policeOfficeName=policeOfficeName,areaCode=areaCode)
                    policeOffice.save()
                else:
                    print(address + " failed 2")
            else:
                print(address + " failed")
    return HttpResponse(csv)