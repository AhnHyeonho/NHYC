from django.db import models


# Create your models here.

class Average(models.Model):
    gu = models.CharField(max_length=50, primary_key=True)
    dong = models.CharField(max_length=50)
    rentalFee = models.IntegerField()
    deposit = models.IntegerField()
    cnt = models.IntegerField()


class Result_GuCnt(models.Model):
    gu = models.CharField(max_length=50, primary_key=True)
    cnt = models.IntegerField()


class Result_GuDongCnt(models.Model):
    gu = models.CharField(max_length=50)
    dong = models.CharField(max_length=50, primary_key=True)
    cnt = models.IntegerField()


class TrendChartData(models.Model):
    date = models.DateField(primary_key=True)
    avg_rentalFee = models.IntegerField()
    avg_deposit = models.IntegerField()
