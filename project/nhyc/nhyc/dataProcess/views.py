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

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from knox.models import AuthToken
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer


from .models import Address
from .models import CCTV
from .models import CostRecord
from .models import FrequentPlace
from .models import HouseInfo
from .models import Member
from .models import MemberInfo
from .models import PoliceOffice
from .models import SecurityLight
from .models import Park
from .models import Market
from .models import Pharmacy
from .models import CulturalFacility
from .models import Library
from .models import ConcertHall
from .models import Gym
from .models import Subway
from .models import Bus

from .managers import CustomUserManager

naverClientId = "tw8yh1kfp6"
naverClientPasswd = "Djx3jNQ1bbXODDxgZM9GS8XL391dPXB2VyxsbO2E"
naverGeocodeURL = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
naverReverseGeocodeURL = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"

@api_view(["GET"])
def HelloAPI(request):
    return Response("hello world!")


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data["memberId"]) < 6 or len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


def getAddress(reqeust):
    data = pandas.read_excel(os.path.join(settings.BASE_DIR, "dataProcess/법정동코드 전체자료.xlsx"))

    data["시"] = data["법정동명"].str.split(" ").str[0]
    data["구"] = data["법정동명"].str.split(" ").str[1]
    data["동"] = data["법정동명"].str.split(" ").str[2]

    data = data.dropna()
    data = data[(data["폐지여부"] == "존재") & (data["시"] == "서울특별시")]
    data = data.reset_index(drop=True, inplace=False)

    for i in data.index:
        areaCode = data.get_value(i, "법정동코드")  # <<<---여기인거 같어
        si = data.get_value(i, "시")
        gu = data.get_value(i, "구")
        dong = data.get_value(i, "동")
        address = Address(areaCode=areaCode, si=si, gu=gu, dong=dong)
        address.save()

    return HttpResponse()

def getDongLatLongs(request):
    addresses = Address.objects.all()
    for address in addresses:
        query = address.si + " " + address.gu + " " + address.dong
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
            address.latitude = latitude
            address.longitude = longitude
            address.save()
    return HttpResponse("끗")


def getHouseInfo(request, start=1, end=4000000):
    url = "http://openapi.seoul.go.kr:8088/545149464a73696c39326f47667644/json/houseRentPriceInfo/"

    while (start != end):
        http = httplib2.Http()
        finalurl = url + str(start) + "/" + str(start + 999)
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
        start = start + 1000

    return HttpResponse("finish")


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

                if (CCTV.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
                    naverURL = naverReverseGeocodeURL + "?coords=" + str(longitude) + "," + str(
                        latitude) + "&orders=legalcode&output=json"
                    https = urllib.request.Request(naverURL)
                    https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                    https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                    response = urllib.request.urlopen(https)
                    content = response.read()
                    content = content.decode("utf-8")

                    addressData = json.loads(content)

                    if addressData["status"]["name"] == "ok":
                        region = addressData["results"][0]["region"]
                        gu = region["area2"]["name"]
                        dong = region["area3"]["name"]
                        print(gu + " " + dong)

            else:
                if pandas.notnull(csv.at[i, "소재지도로명주소"]):
                    address = csv.at[i, "소재지도로명주소"]
                elif pandas.notnull(csv.at[i, "소재지지번주소"]):
                    address = csv.at[i, "소재지지번주소"]

                print(address)
                if pandas.notnull(address):
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
                        if len(addressSplit) > 2:
                            gu = addressSplit[1]
                            dong = addressSplit[2]

            if Address.objects.filter(gu=gu, dong=dong).count() == 1:
                areaCode = Address.objects.get(gu=gu, dong=dong)
                if CCTV.objects.filter(latitude=latitude, longitude=longitude).count() == 0:
                    cctv = CCTV(latitude=latitude, longitude=longitude, areaCode=areaCode)
                    cctv.save()

    return HttpResponse(csv)


def getSecurityLight(request, filename=None):
    cctvPath = os.path.join(settings.BASE_DIR, "dataProcess", "보안등")
    if filename == None:
        fileList = os.listdir(cctvPath)
    else:
        fileList = {filename}

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

                    if addressData["status"]["name"] == "ok":
                        region = addressData["results"][0]["region"]
                        gu = region["area2"]["name"]
                        dong = region["area3"]["name"]
                        print(gu + " " + dong)

            else:
                if pandas.notnull(csv.at[i, "소재지도로명주소"]):
                    address = csv.at[i, "소재지도로명주소"]
                elif pandas.notnull(csv.at[i, "소재지지번주소"]):
                    address = csv.at[i, "소재지지번주소"]

                print(address)
                if pandas.notnull(address):
                    naverURL = naverGeocodeURL + "?query=" + quote(address)
                    https = urllib.request.Request(naverURL)
                    https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                    https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                    response = urllib.request.urlopen(https)
                    content = response.read()
                    content = content.decode("utf-8")

                    geocode = json.loads(content)
                    if "meta" in geocode and geocode["meta"]["count"] != 0:
                        latitude = geocode["addresses"][0]["y"]
                        longitude = geocode["addresses"][0]["x"]
                        addressSplit = geocode["addresses"][0]["jibunAddress"].split()
                        if len(addressSplit) > 2:
                            gu = addressSplit[1]
                            dong = addressSplit[2]
            if Address.objects.filter(gu=gu, dong=dong).count() == 1:
                areaCode = Address.objects.get(gu=gu, dong=dong)
                if SecurityLight.objects.filter(latitude=latitude, longitude=longitude).count() == 0:
                    securityLight = SecurityLight(latitude=latitude, longitude=longitude, areaCode=areaCode)
                    securityLight.save()

    return HttpResponse(csv)


def getPoliceOffice(request):
    csv = pandas.read_csv(os.path.join(settings.BASE_DIR, "dataProcess/경찰관서위치_20200409.csv"), encoding="CP949")
    csv = csv.dropna()
    csv = csv[csv["청"].str.contains("서울")]

    for i in csv.index:
        latitude = csv.at[i, "Y좌표"]
        longitude = csv.at[i, "X좌표"]

        if (PoliceOffice.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
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
                areaCode = Address.objects.get(gu=gu, dong=dong)
                policeOfficeName = csv.get_value(i, "지구대파출소")
                policeOffice = PoliceOffice(latitude=latitude, longitude=longitude, policeOfficeName=policeOfficeName,
                                            areaCode=areaCode)
                policeOffice.save()

    return HttpResponse(csv)


def getPark(request):
    csv = pandas.read_csv(os.path.join(settings.BASE_DIR, "dataProcess/1전국도시공원정보표준데이터.csv"), encoding="CP949")
    csv = csv[csv["소재지도로명주소"].str.contains("서울") & csv["소재지지번주소"].str.contains("서울")]

    for i in csv.index:
        gu = ""
        dong = ""
        if pandas.notnull(csv.at[i, "위도"]) and pandas.notnull(csv.at[i, "경도"]):
            latitude = csv.at[i, "위도"]
            longitude = csv.at[i, "경도"]
            parkName = csv.at[i, "공원명"]

            if (Park.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
                naverURL = naverReverseGeocodeURL + "?coords=" + str(longitude) + "," + str(
                    latitude) + "&orders=legalcode&output=json"
                https = urllib.request.Request(naverURL)
                https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                response = urllib.request.urlopen(https)
                content = response.read()
                content = content.decode("utf-8")

                addressData = json.loads(content)

                if addressData["status"]["name"] == "ok":
                    region = addressData["results"][0]["region"]
                    gu = region["area2"]["name"]
                    dong = region["area3"]["name"]
                    print(gu + " " + dong)

        else:
            if pandas.notnull(csv.at[i, "소재지도로명주소"]):
                address = csv.at[i, "소재지도로명주소"]
            elif pandas.notnull(csv.at[i, "소재지지번주소"]):
                address = csv.at[i, "소재지지번주소"]

            print(address)
            if pandas.notnull(address):
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
                    if len(addressSplit) > 2:
                        gu = addressSplit[1]
                        dong = addressSplit[2]
        if Address.objects.filter(gu=gu, dong=dong).count() == 1:
            areaCode = Address.objects.get(gu=gu, dong=dong)
            if Park.objects.filter(latitude=latitude, longitude=longitude).count() == 0:
                park = Park(latitude=latitude, longitude=longitude, parkName=parkName, areaCode=areaCode)
                park.save()

    return HttpResponse(csv)


def getMarket(request):
    csv = pandas.read_csv(os.path.join(settings.BASE_DIR, "dataProcess/2전국전통시장표준데이터.csv"), encoding="CP949")
    csv = csv[csv["소재지도로명주소"].str.contains("서울") & csv["소재지지번주소"].str.contains("서울")]

    for i in csv.index:
        gu = ""
        dong = ""
        if pandas.notnull(csv.at[i, "위도"]) and pandas.notnull(csv.at[i, "경도"]):
            latitude = csv.at[i, "위도"]
            longitude = csv.at[i, "경도"]
            marketName = csv.at[i, "시장명"]

            if (Market.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
                naverURL = naverReverseGeocodeURL + "?coords=" + str(longitude) + "," + str(
                    latitude) + "&orders=legalcode&output=json"
                https = urllib.request.Request(naverURL)
                https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                response = urllib.request.urlopen(https)
                content = response.read()
                content = content.decode("utf-8")

                addressData = json.loads(content)

                if addressData["status"]["name"] == "ok":
                    region = addressData["results"][0]["region"]
                    gu = region["area2"]["name"]
                    dong = region["area3"]["name"]
                    print(gu + " " + dong)

        else:
            if pandas.notnull(csv.at[i, "소재지도로명주소"]):
                address = csv.at[i, "소재지도로명주소"]
            elif pandas.notnull(csv.at[i, "소재지지번주소"]):
                address = csv.at[i, "소재지지번주소"]

            print(address)
            if pandas.notnull(address):
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
                    if len(addressSplit) > 2:
                        gu = addressSplit[1]
                        dong = addressSplit[2]
        if Address.objects.filter(gu=gu, dong=dong).count() == 1:
            areaCode = Address.objects.get(gu=gu, dong=dong)
            if Market.objects.filter(latitude=latitude, longitude=longitude).count() == 0:
                market = Market(latitude=latitude, longitude=longitude, marketName=marketName, areaCode=areaCode)
                market.save()

    return HttpResponse(csv)


def getPharmacy(request):
    csv = pandas.read_csv(os.path.join(settings.BASE_DIR, "dataProcess/3서울특별시 약국정보.csv"), encoding="CP949")
    csv = csv[csv["소재지전체주소"].str.contains("서울") & csv["도로명전체주소"].str.contains("서울")]

    for i in csv.index:
        gu = ""
        dong = ""
        pharmacyName = csv.at[i, "사업장명"]
        if pandas.notnull(csv.at[i, "소재지전체주소"]):
            address = csv.at[i, "소재지전체주소"]
        elif pandas.notnull(csv.at[i, "도로명전체주소"]):
            address = csv.at[i, "도로명전체주소"]

        print(address)
        if pandas.notnull(address):
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
                if len(addressSplit) > 2:
                    gu = addressSplit[1]
                    dong = addressSplit[2]
        if Address.objects.filter(gu=gu, dong=dong).count() == 1:
            areaCode = Address.objects.get(gu=gu, dong=dong)
            if Pharmacy.objects.filter(latitude=latitude, longitude=longitude).count() == 0:
                pharmacy = Pharmacy(latitude=latitude, longitude=longitude, pharmacyName=pharmacyName,
                                    areaCode=areaCode)
                pharmacy.save()

    return HttpResponse(csv)


def getCulturalFacility(request):
    csv = pandas.read_csv(os.path.join(settings.BASE_DIR, "dataProcess/4전국박물관미술관정보표준데이터.csv"), encoding="CP949")
    csv = csv[csv["소재지도로명주소"].str.contains("서울") & csv["소재지지번주소"].str.contains("서울")]

    for i in csv.index:
        gu = ""
        dong = ""
        if pandas.notnull(csv.at[i, "위도"]) and pandas.notnull(csv.at[i, "경도"]):
            latitude = csv.at[i, "위도"]
            longitude = csv.at[i, "경도"]
            culturalFacilityName = csv.at[i, "시설명"]

            if (CulturalFacility.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
                naverURL = naverReverseGeocodeURL + "?coords=" + str(longitude) + "," + str(
                    latitude) + "&orders=legalcode&output=json"
                https = urllib.request.Request(naverURL)
                https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                response = urllib.request.urlopen(https)
                content = response.read()
                content = content.decode("utf-8")

                addressData = json.loads(content)

                if addressData["status"]["name"] == "ok":
                    region = addressData["results"][0]["region"]
                    gu = region["area2"]["name"]
                    dong = region["area3"]["name"]
                    print(gu + " " + dong)

        else:
            if pandas.notnull(csv.at[i, "소재지도로명주소"]):
                address = csv.at[i, "소재지도로명주소"]
            elif pandas.notnull(csv.at[i, "소재지지번주소"]):
                address = csv.at[i, "소재지지번주소"]

            print(address)
            if pandas.notnull(address):
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
                    if len(addressSplit) > 2:
                        gu = addressSplit[1]
                        dong = addressSplit[2]
        if Address.objects.filter(gu=gu, dong=dong).count() == 1:
            areaCode = Address.objects.get(gu=gu, dong=dong)
            if CulturalFacility.objects.filter(latitude=latitude, longitude=longitude).count() == 0:
                culturalFacility = CulturalFacility(latitude=latitude, longitude=longitude,
                                                    culturalFacilityName=culturalFacilityName, areaCode=areaCode)
                culturalFacility.save()

    return HttpResponse(csv)


def getLibrary(request):
    csv = pandas.read_csv(os.path.join(settings.BASE_DIR, "dataProcess/5전국도서관표준데이터.csv"), encoding="CP949")
    csv = csv[csv["소재지도로명주소"].str.contains("서울")]

    for i in csv.index:
        gu = ""
        dong = ""
        if pandas.notnull(csv.at[i, "위도"]) and pandas.notnull(csv.at[i, "경도"]):
            latitude = csv.at[i, "위도"]
            longitude = csv.at[i, "경도"]
            libraryName = csv.at[i, "도서관명"]

            if (Library.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
                naverURL = naverReverseGeocodeURL + "?coords=" + str(longitude) + "," + str(
                    latitude) + "&orders=legalcode&output=json"
                https = urllib.request.Request(naverURL)
                https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                response = urllib.request.urlopen(https)
                content = response.read()
                content = content.decode("utf-8")

                addressData = json.loads(content)

                if addressData["status"]["name"] == "ok":
                    region = addressData["results"][0]["region"]
                    gu = region["area2"]["name"]
                    dong = region["area3"]["name"]
                    print(gu + " " + dong)

        else:
            if pandas.notnull(csv.at[i, "소재지도로명주소"]):
                address = csv.at[i, "소재지도로명주소"]

            print(address)
            if pandas.notnull(address):
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
                    if len(addressSplit) > 2:
                        gu = addressSplit[1]
                        dong = addressSplit[2]
        if Address.objects.filter(gu=gu, dong=dong).count() == 1:
            areaCode = Address.objects.get(gu=gu, dong=dong)
            if Library.objects.filter(latitude=latitude, longitude=longitude).count() == 0:
                library = Library(latitude=latitude, longitude=longitude, libraryName=libraryName, areaCode=areaCode)
                library.save()

    return HttpResponse(csv)


def getConcertHall(request):
    csv = pandas.read_csv(os.path.join(settings.BASE_DIR, "dataProcess/6서울시 공연장 현황.csv"), encoding="CP949")
    csv = csv.dropna(subset=["공연장소재지(지번)"])
    csv = csv[csv["공연장소재지(지번)"].str.contains("서울")]

    for i in csv.index:
        gu = ""
        dong = ""
        concertHallName = csv.at[i, "공연장명칭"]
        if pandas.notnull(csv.at[i, "공연장소재지(지번)"]):
            address = csv.at[i, "공연장소재지(지번)"]

        print(address)
        if pandas.notnull(address):
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
                if len(addressSplit) > 2:
                    gu = addressSplit[1]
                    dong = addressSplit[2]
        if Address.objects.filter(gu=gu, dong=dong).count() == 1:
            areaCode = Address.objects.get(gu=gu, dong=dong)
            if ConcertHall.objects.filter(latitude=latitude, longitude=longitude).count() == 0:
                concertHall = ConcertHall(latitude=latitude, longitude=longitude, concertHallName=concertHallName,
                                          areaCode=areaCode)
                concertHall.save()

    return HttpResponse(csv)


def getGym(request):
    csv = pandas.read_csv(os.path.join(settings.BASE_DIR, "dataProcess/7서울시 공공체육시설 현황(2019).csv"), encoding="CP949")

    for i in csv.index:
        gu = ""
        dong = ""
        if pandas.notnull(csv.at[i, "위도"]) and pandas.notnull(csv.at[i, "경도"]):
            latitude = csv.at[i, "위도"]
            longitude = csv.at[i, "경도"]
            gymName = csv.at[i, "시설명"]

            if (Gym.objects.filter(latitude=latitude, longitude=longitude).count() == 0):
                naverURL = naverReverseGeocodeURL + "?coords=" + str(longitude) + "," + str(
                    latitude) + "&orders=legalcode&output=json"
                https = urllib.request.Request(naverURL)
                https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                response = urllib.request.urlopen(https)
                content = response.read()
                content = content.decode("utf-8")

                addressData = json.loads(content)

                if addressData["status"]["name"] == "ok":
                    region = addressData["results"][0]["region"]
                    gu = region["area2"]["name"]
                    dong = region["area3"]["name"]
                    print(gu + " " + dong)

        else:
            if pandas.notnull(csv.at[i, "주소"]):
                address = csv.at[i, "주소"]

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
                    if len(addressSplit) > 2:
                        gu = addressSplit[1]
                        dong = addressSplit[2]
        if Address.objects.filter(gu=gu, dong=dong).count() == 1:
            areaCode = Address.objects.get(gu=gu, dong=dong)
            if Gym.objects.filter(latitude=latitude, longitude=longitude).count() == 0:
                gym = Gym(latitude=latitude, longitude=longitude, gymName=gymName, areaCode=areaCode)
                gym.save()

    return HttpResponse(csv)


def getSubway(request):
    url = "http://openapi.seoul.go.kr:8088/777a6e687273696c35386152625747/json/SearchInfoBySubwayNameService/1/1000"
    subwayUrl = "http://openapi.seoul.go.kr:8088/777a6e687273696c35386152625747/json/SearchLocationOfSTNByIDService/1/1/"
    http = httplib2.Http()
    response, content = http.request(url, "GET")
    content = content.decode("utf-8")
    jsonData = json.loads(content)

    code = jsonData["SearchInfoBySubwayNameService"]["RESULT"]["CODE"]
    if code == "INFO-000":
        datas = jsonData["SearchInfoBySubwayNameService"]["row"]
        for data in datas:
            http2 = httplib2.Http()
            res, cont = http2.request(subwayUrl + data["STATION_CD"], "GET")
            cont = cont.decode("utf-8")
            info = json.loads(cont)

            if "SearchLocationOfSTNByIDService" in info and info["SearchLocationOfSTNByIDService"]["RESULT"][
                "CODE"] == "INFO-000":
                latitude = info["SearchLocationOfSTNByIDService"]["row"][0]["XPOINT_WGS"]
                longitude = info["SearchLocationOfSTNByIDService"]["row"][0]["YPOINT_WGS"]
                subwayName = info["SearchLocationOfSTNByIDService"]["row"][0]["STATION_NM"]
                line = data["LINE_NUM"]

                if latitude != "" and longitude != "" and Subway.objects.filter(latitude=latitude,
                                                                                longitude=longitude).count() == 0:
                    naverURL = naverReverseGeocodeURL + "?coords=" + str(longitude) + "," + str(
                        latitude) + "&orders=legalcode&output=json"
                    https = urllib.request.Request(naverURL)
                    https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                    https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                    r = urllib.request.urlopen(https)
                    c = r.read()
                    c = c.decode("utf-8")

                    addressData = json.loads(c)

                    if addressData["status"]["name"] == "ok":
                        region = addressData["results"][0]["region"]
                        gu = region["area2"]["name"]
                        dong = region["area3"]["name"]
                        print(gu + " " + dong)

                        if Address.objects.filter(gu=gu, dong=dong).count() == 1:
                            areaCode = Address.objects.get(gu=gu, dong=dong)
                            subway = Subway(latitude=latitude, longitude=longitude, subwayName=subwayName, line=line,
                                            areaCode=areaCode)
                            subway.save()

    return HttpResponse("지하철 역 끝")


def getBus(request, start = 1):
    url = "http://openapi.seoul.go.kr:8088/575447434f73696c3131336e52426f4d/json/busStopLocationXyInfo/"
    end = start + 999

    while (True):
        http = httplib2.Http()
        response, content = http.request(url + str(start) + "/" + str(end), "GET")
        content = content.decode("utf-8")
        jsonData = json.loads(content)

        code = jsonData["busStopLocationXyInfo"]["RESULT"]["CODE"]
        if code == "INFO-000":
            datas = jsonData["busStopLocationXyInfo"]["row"]
            for data in datas:
                latitude = data["YCODE"]
                longitude = data["XCODE"]
                stationName = data["STOP_NM"]

                if latitude != "" and longitude != "" and Bus.objects.filter(latitude=latitude,
                                                                             longitude=longitude).count() == 0:
                    naverURL = naverReverseGeocodeURL + "?coords=" + str(longitude) + "," + str(
                        latitude) + "&orders=legalcode&output=json"
                    https = urllib.request.Request(naverURL)
                    https.add_header("X-NCP-APIGW-API-KEY-ID", naverClientId)
                    https.add_header("X-NCP-APIGW-API-KEY", naverClientPasswd)
                    r = urllib.request.urlopen(https)
                    c = r.read()
                    c = c.decode("utf-8")

                    addressData = json.loads(c)

                    if addressData["status"]["name"] == "ok":
                        region = addressData["results"][0]["region"]
                        gu = region["area2"]["name"]
                        dong = region["area3"]["name"]
                        print(gu + " " + dong)

                        if Address.objects.filter(gu=gu, dong=dong).count() == 1:
                            areaCode = Address.objects.get(gu=gu, dong=dong)
                            bus = Bus(latitude=latitude, longitude=longitude, stationName=stationName, areaCode=areaCode)
                            bus.save()
        if len(datas) < 1000:
            break;
        print(start)
        start = start + 1000
        end = end + 1000

    return HttpResponse("버스 정류장 끝")
