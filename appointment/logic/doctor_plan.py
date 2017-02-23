# -*- coding: UTF-8 -*-
from django.core.mail import send_mail

from appointment.logic.appointment_time import *
from appointment.logic.appointment_time import sort_appointment_times_in_day
from appointment.models import AppointmentTime


def get_doctor_all_plan(start_date, doctor):
    """
    :param start_date: start time
    :param doctor: doctor
    :return: list of doctor plan from a given time to end
    """
    apps = [app for app in AppointmentTime.objects.filter(doctor=doctor) if
            (app.date >= start_date and app.confirmation != '2')]

    apps = sort_appointment_times(apps)
    return cluster_appointment_times(apps)


def get_doctor_day_plan(date, doctor):
    return sort_appointment_times_in_day(
        list(AppointmentTime.objects.filter(doctor=doctor, date=date, confirmation__in=['1', '3'])))


def send_app_reserve_mail(app):
    title = 'نوبت جدید توسط بیمار'
    body = ' با سلام \n بیمار' + str(app.patient.user.first_name) + ' ' + str(
        app.patient.user.last_name) + ' در تاریخ ' + str(app.date) + ' ساعت  ' + str(
        app.start_time) + 'از شما تقاضای نوبت کرده است. لطفا در صورت موافقت این نوبت را تایید فرمایید.'
    send_mail(title, body, 'onlinefoodforyou@gmail.com', [app.doctor.user.user.email], fail_silently=True)
