from django.db import models

class Address(models.Model):
    sido = models.CharField(max_length=100)
    sigungu = models.CharField(max_length=100)
    eupmyeondong = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sido} {self.sigungu} {self.eupmyeondong}"

class University(models.Model):
    univ_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.univ_name