from django.db import models

class Member(models.Model):
    id = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.id

class Address(models.Model):
    areaCode = models.CharField(max_length=10)
    si = models.CharField(max_length=50)
    gu = models.CharField(max_length=50)
    dong = models.CharField(max_length=50)

class MemberInfo(models.Model):
    id = models.ForeignKey('Member', on_delete=models.CASCADE)
    gender = models.CharField(max_length=1)
    birth = models.IntegerField(max_length=4)
    money = models.IntegerField()

    def __str__(self):
        return self.id

class FrequentPlace(models.Model):
    id = models.ForeignKey('Member', on_delete=models.CASCADE)
    placeName = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.placeName

class HouseInfo(models.Model):
    houseNumber = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    pyeong = models.FloatField()
    houseName = models.CharField(max_length=100)
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.houseName

class CostRecord(models.Model):
    houseNumber = models.ForeignKey('HouseInfo', on_delete=models.CASCADE)
    day = models.DateField()
    rentalFee = models.IntegerField()
    deposit = models.IntegerField()

    def __str__(self):
        return [self.day, self.rentalFee, self.deposit]

class CCTV(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return [self.latitude, self.longitude]

class SecurityLight(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return [self.latitude, self.longitude]

class PoliceOffice(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    policeOfficeName = models.CharField(max_length=50)
    areaCode = models.ForeignKey('Address', on_delete=models.CASCADE)

    def __str__(self):
        return self.policeOfficeName