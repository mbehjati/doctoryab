# Create your models here.
from django.db import models

from user.models import Doctor, MyUser


class AppointmentTime(models.Model):
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=8)
    duration = models.IntegerField()
    doctor = models.ForeignKey(Doctor)
    patient = models.ForeignKey(MyUser, null=True)

    def __str__(self):
        return "doctor " + str(self.doctor.user.user.username) + " " + str(self.date) + " " + str(self.time)

    def __eq__(self, other):
        return self.date == other.date and self.time == other.time and self.duration == other.duration and self.doctor == other.doctor and self.patient == other.patient

