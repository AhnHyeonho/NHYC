from django.shortcuts import render
import json, httplib2

from .models import Member
from .models import Address
from .models import MemberInfo
from .models import FrequentPlace
from .models import HouseInfo
from .models import CostRecord
from .models import CCTV
from .models import SecurityLight
from .models import PoliceOffice

def getHouseInfo(request):
    url = "http://openapi.seoul.go.kr:8088/545149464a73696c39326f47667644/json/houseRentPriceInfo/"
    start = 1
    end = 1000

    while(True):
        conn = httplib2.