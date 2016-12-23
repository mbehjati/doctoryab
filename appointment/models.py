# Create your models here.
from django.db import models

from user.models import Doctor , MyUser


class AppointmentTime(models.Model):
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()
    doctor = models.ForeignKey(Doctor)
    patient = models.ForeignKey(MyUser , null=True)
