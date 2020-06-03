from django.db import models


# Create your models here.

class Average(models.Model):
    gu = models.CharField(max_length=50, primary_key=True)
    rentalFee = models.IntegerField()
    deposit = models.IntegerField()


class Result_GuCnt(models.Model):
    gu = models.CharField(max_length=50, primary_key=True)
    cnt = models.IntegerField()


class Result_GuDongCnt(models.Model):
    gu = models.CharField(max_length=50)
    dong = models.CharField(max_length=50, primary_key=True)
    cnt = models.IntegerField()

