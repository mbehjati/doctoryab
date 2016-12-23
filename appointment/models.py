# Create your models here.
from django.db import models

from user.models import Doctor , MyUser


class AppointmentTime(models.Model):
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()
    doctor = models.ForeignKey(Doctor)
    patient = models.ForeignKey(MyUser , null=True)

class Insurance (models.Model):
    name  = models.TextField(primary_key=True)

class Expertise(models.Model):
    name = models.TextField(primary_key=True)