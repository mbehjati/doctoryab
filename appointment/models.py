# -*- coding: UTF-8 -*-

from django.db import models

from user.models import Doctor, MyUser


class AppointmentTime(models.Model):
    date = models.CharField(max_length=20)
    start_time = models.CharField(max_length=8)
    end_time = models.CharField(max_length=8)
    duration = models.IntegerField()
    doctor = models.ForeignKey(Doctor)
    patient = models.ForeignKey(MyUser, null=True)
    confirmation = models.CharField(max_length=1, default='1',
                                    choices=(('1', 'awaiting'), ('2', 'not_confirmed'), ('3', 'confirmed')))
    presence = models.BooleanField(default=False)

    def __str__(self):
        return "doctor " + str(self.doctor.user.user.username) + " " + str(self.date) + " " + str(self.start_time)

    def __eq__(self, other):
        return self.date == other.date and self.start_time == other.start_time and self.duration == other.duration and \
               self.doctor == other.doctor and self.patient == other.patient

    def get_status(self):  # TODO: write test for this part
        status = ['در انتظار تایید', 'تایید نشده', 'تایید شده']
        return status[int(self.confirmation)]
