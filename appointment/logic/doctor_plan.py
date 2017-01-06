# -*- coding: UTF-8 -*-

from appointment.logic.appointment_time import *
from appointment.logic.appointment_time import sort_appointment_times_in_day
from appointment.models import AppointmentTime


def get_doctor_all_plan(start_date, doctor):
    apps = []
    for app in AppointmentTime.objects.filter(doctor=doctor):
        if app.date >= start_date:
            apps.append(app)
    apps = sort_appointment_times(apps)
    return cluster_appointment_times(apps)


def get_doctor_day_plan(date, doctor):
    return sort_appointment_times_in_day(list(AppointmentTime.objects.filter(doctor=doctor, date=date)))
