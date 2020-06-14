from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class Member(AbstractUser):
    memberId = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=300)
    name = models.CharField(max_length=50)

    USERNAME_FIELD = 'memberId'
    REQUIRED_FIELDS = ['email', 'name']

    objects = CustomUserManager()

    def __str__(self):
        return self.id

class Gu(models.Model):
    areaCode = models.CharField(max_length=10, primary_key=True)
    si = models.CharField(max_length=50)
    gu = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.areaCode


class Address(models.Model):
    areaCode = models.CharField(max_length=10, primary_key=True)
    si = models.CharField(max_length=50)
    gu = models.CharField(max_length=50)
    dong = models.CharField(max_length=50)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.areaCode


class MemberInfo(models.Model):
    member = models.OneToOneField('Member', on_delete=models.CASCADE, default=None)
    gender = models.CharField(max_length=1, null=True)
    age_range = models.CharField(max_length=10, null=True)
    rentalFee = models.IntegerField(null=True)
    deposit = models.IntegerField(null=True)

    def __str__(self):
        return self.member.id


class MemberTrend(models.Model):
    member = models.OneToOneField('Member', on_delete=models.CASCADE, default=None)
    budget = models.IntegerField(default=0)
    safety = models.IntegerField(default=0)
    life = models.IntegerField(default=0)
    culture = models.IntegerField(default=0)
    transportation = models.IntegerField(default=0)

    def __str__(self):
        return self.member.id

class RecommendedDong(models.Model):
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)
    pointOfBudget = models.FloatField()
    pointOfSafety = models.FloatField()
    pointOfLife = models.FloatField()
    pointOfCulture = models.FloatField()
    pointOfTransportation = models.FloatField()

class Recommendation(models.Model):
    memberTrend = models.ForeignKey('MemberTrend', on_delete=models.CASCADE)
    pointOfBudget = models.FloatField()
    pointOfSafety = models.FloatField()
    pointOfLife = models.FloatField()
    pointOfCulture = models.FloatField()
    pointOfTransportation = models.FloatField()
    dong1 = models.ForeignKey('RecommendedDong', on_delete=models.CASCADE, related_name="dong1")
    dong2 = models.ForeignKey('RecommendedDong', on_delete=models.CASCADE, related_name="dong2")
    dong3 = models.ForeignKey('RecommendedDong', on_delete=models.CASCADE, related_name="dong3")
    dong4 = models.ForeignKey('RecommendedDong', on_delete=models.CASCADE, related_name="dong4")
    dong5 = models.ForeignKey('RecommendedDong', on_delete=models.CASCADE, related_name="dong5")

class TrendBySession(models.Model):
    sessionId = models.CharField(max_length=255, primary_key=True)
    budget = models.IntegerField(default=0)
    safety = models.IntegerField(default=0)
    life = models.IntegerField(default=0)
    culture = models.IntegerField(default=0)
    transportation = models.IntegerField(default=0)

    def __str__(self):
        return self.member.id


class FrequentPlace(models.Model):
    placeId = models.AutoField(primary_key=True)
    id = models.ForeignKey('Member', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    placeName = models.CharField(max_length=100)
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.placeName


class HouseInfo(models.Model):
    houseNumber = models.CharField(max_length=19, primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    pyeong = models.FloatField()
    houseName = models.CharField(max_length=100)
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.houseName


class CostRecord(models.Model):
    costRecordId = models.CharField(max_length=25, primary_key=True, default="0")
    houseNumber = models.ForeignKey('HouseInfo', on_delete=models.CASCADE)
    day = models.DateField()
    rentalFee = models.IntegerField()
    deposit = models.IntegerField()

    def __str__(self):
        return [self.day, self.rentalFee, self.deposit]


class CCTV(models.Model):
    cctvId = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return [self.latitude, self.longitude]


class SecurityLight(models.Model):
    lightId = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return [self.latitude, self.longitude]


class PoliceOffice(models.Model):
    policeId = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    policeOfficeName = models.CharField(max_length=50)
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.policeOfficeName


class Park(models.Model):
    parkId = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    parkName = models.CharField(max_length=50)
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.parkName


class Market(models.Model):
    marketId = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    marketName = models.CharField(max_length=50)
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.marketName


class Pharmacy(models.Model):
    pharmacyId = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    pharmacyName = models.CharField(max_length=50)
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.pharmacyName


class CulturalFacility(models.Model):
    culturalFacilityId = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    culturalFacilityName = models.CharField(max_length=50)
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.culturalFacilityName


class Library(models.Model):
    libraryId = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    libraryName = models.CharField(max_length=50)
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.libraryName


class ConcertHall(models.Model):
    concertHallId = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    concertHallName = models.CharField(max_length=50)
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.concertHallName


class Gym(models.Model):
    gymId = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    gymName = models.CharField(max_length=50)
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.gymName


class AddressInfo(models.Model):
    areaCode = models.CharField(max_length=10, primary_key=True)
    si = models.CharField(max_length=50)
    gu = models.CharField(max_length=50)
    dong = models.CharField(max_length=50)
    avgRentalFee = models.FloatField(null=True)
    avgDeposit = models.FloatField(null=True)
    itemCnt = models.IntegerField(null=True)
    totCCTV = models.IntegerField(null=True)
    totPolice = models.IntegerField(null=True)
    totLight = models.IntegerField(null=True)
    totPharmacy = models.IntegerField(null=True)
    totMarket = models.IntegerField(null=True)
    totPark = models.IntegerField(null=True)
    totGym = models.IntegerField(null=True)
    totConcertHall = models.IntegerField(null=True)
    totLibrary = models.IntegerField(null=True)
    totCulturalFacility = models.IntegerField(null=True)
    totSubway = models.IntegerField(null=True)
    totBus = models.IntegerField(null=True)
    rateCCTV = models.FloatField(null=True)
    ratePolice = models.FloatField(null=True)
    rateLight = models.FloatField(null=True)
    ratePharmacy = models.FloatField(null=True)
    rateMarket = models.FloatField(null=True)
    ratePark = models.FloatField(null=True)
    rateGym = models.FloatField(null=True)
    rateConcertHall = models.FloatField(null=True)
    rateLibrary = models.FloatField(null=True)
    rateCulturalFacility = models.FloatField(null=True)
    rateSubway = models.FloatField(null=True)
    rateBus = models.FloatField(null=True)

    def __str__(self):
        return self.areaCode

class Subway(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    subwayName = models.CharField(max_length=50)
    line = models.CharField(max_length=50)
    areaCode = models.ForeignKey("Address", on_delete=models.CASCADE)

class Bus(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    stationName = models.CharField(max_length=50)
    areaCode = models.ForeignKey("Address", on_delete=models.CASCADE)
