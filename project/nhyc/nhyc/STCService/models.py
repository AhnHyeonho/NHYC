from django.db import models


# Create your models here.

class Average(models.Model):
    gu = models.CharField(max_length=50)
    rentalFee = models.IntegerField()
    deposit = models.IntegerField()
