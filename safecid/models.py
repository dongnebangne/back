from django.db import models

class Address(models.Model):
    sido = models.CharField(max_length=100)
    sigungu = models.CharField(max_length=100)
    eupmyeondong = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sido} {self.sigungu} {self.eupmyeondong}"