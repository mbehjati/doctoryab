# Create your models here.
from django.db import models


class VisitTime(models.Model):
    date = models.DateField(primary_key=True)
    time = models.TimeField(primary_key=True)
    duration = models.IntegerField()
    # TODO doctor
    # patient =
