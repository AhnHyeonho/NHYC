from django.db import models

class Member(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.id

class Address(models.Model):
    areaCode = models.CharField(max_length=10, primary_key=True)
    si = models.CharField(max_length=50)
    gu = models.CharField(max_length=50)
    dong = models.CharField(max_length=50)
    def __str__(self):
        return self.areaCode

class MemberInfo(models.Model):
    member = models.OneToOneField('Member', on_delete=models.CASCADE, default=None)
    gender = models.CharField(max_length=1)
    birth = models.CharField(max_length=4)
    money = models.IntegerField()

    def __str__(self):
        return self.id

class FrequentPlace(models.Model):
    placeId = models.IntegerField(primary_key=True)
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