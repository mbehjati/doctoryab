# Create your models here.
from django.db import models

from user.models import Doctor , MyUser


class AppointmentTime(models.Model):
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=8)
    duration = models.IntegerField()
    doctor = models.ForeignKey(Doctor)
    patient = models.ForeignKey(MyUser, null=True)

    def __str__(self):
        return "doctor " + str(self.doctor.user.user.username) + " " + str(self.date) + " " + str(self.time)


class Insurance (models.Model):
    name = models.TextField(primary_key=True)

    def __str__(self):
        return self.name


class Expertise(models.Model):
    name = models.TextField(primary_key=True)

    def __str__(self):
        return self.name