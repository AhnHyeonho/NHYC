# STCService(ServerToClient)/serializers.py

from rest_framework import serializers
from dataProcess.models import Member
from dataProcess.models import Address
from dataProcess.models import MemberInfo
from dataProcess.models import HouseInfo
from dataProcess.models import FrequentPlace
from dataProcess.models import CostRecord
from dataProcess.models import CCTV
from dataProcess.models import SecurityLight
from dataProcess.models import PoliceOffice


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = (
            'id',
            'password',
            'name'
        )


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'areaCode',
            'si',
            'gu',
            'dong'
        )


class MemberInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberInfo
        fields = (
            'member',
            'gender',
            'birth',
            'money'
        )


class FrequentPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentPlace
        fields = (
            'placeId',
            'id',
            'latitude',
            'longitude',
            'placeName',
            'areaCode_id'
        )


class HouseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseInfo
        fields = (
            'houseNumber',
            'latitude',
            'longitude',
            'pyeong',
            'houseName',
            'areaCode_id'
        )


class CostRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostRecord
        fields = (
            'costRecord',
            'houseNumber',
            'day',
            'rentalFee',
            'deposit'
        )


class CCTVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCTV
        fields = (
            'cctvId',
            'latitude',
            'longitude',
            'areaCode_id'
        )


class SecurityLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityLight
        fields = (
            'lightId',
            'latitude',
            'longitude',
            'areaCode_id'
        )


class PoliceOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceOffice
        fields = (
            'policeId',
            'latitude',
            'longitude',
            'policeOfficeName',
            'areaCode_id'
        )
