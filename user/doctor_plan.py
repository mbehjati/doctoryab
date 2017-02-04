# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta

import jdatetime
from django.core.mail import send_mail

from appointment.logic.appointment_time import is_time_before, add_time
from appointment.logic.doctor_plan import get_doctor_day_plan
from appointment.models import AppointmentTime
from user.lib.jalali import Gregorian


def save_doctor_free_times_in_db(doctor, form):
    for obj in calc_doctor_free_times(doctor, form):
        if not has_appointment_conflict(obj, AppointmentTime.objects.filter(confirmation__in=['1', '3'])):
            obj.save()


def calc_doctor_free_times(doctor, form):
    '''
    :param doctor: doctor
    :param form: form of doctor free time
    :return: a list of AppointmentTime objects for doctor created base on from information
    '''
    start_date = datetime.strptime(form.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(form.end_date, '%Y-%m-%d')
    day = timedelta(days=1)
    ans = []

    while start_date <= end_date:
        ans.extend(calc_visit_times_for_a_day(doctor, str(start_date.date()), form.start_time, form.end_time,
                                              form.visit_duration))
        start_date = start_date + day
    return ans


def has_appointment_conflict(appointment, all_apps):
    '''

    :param appointment: an appointment
    :param all_apps: a list of appointments
    :return: true if given appointment has time conflict with list of appointments
    '''
    for app in all_apps:
        if app.doctor == appointment.doctor:
            if app.date == appointment.date:
                if not ((is_time_before(appointment.start_time, app.start_time) and is_time_before(appointment.end_time,
                                                                                                   app.start_time)) or (
                            is_time_before(app.end_time, appointment.start_time) and is_time_before(app.end_time,
                                                                                                    appointment.end_time))):
                    return True
    return False


def calc_visit_times_for_a_day(doctor, day, start_time, end_time, duration):
    ans = []
    while is_time_before(add_time(start_time, duration), end_time):
        ans.append(
            AppointmentTime(date=day, start_time=start_time, end_time=add_time(start_time, duration), duration=duration,
                            doctor=doctor))
        start_time = add_time(start_time, duration)
    return ans


def send_app_result_mail(app, confirm):
    action = 'تایید' if confirm else 'رد'
    title = action + ' نوبت'
    body = ' با سلام \n نوبت شما از دکتر' + str(app.doctor.user.user.first_name) + ' ' + str(
        app.doctor.user.user.last_name) + ' در تاریخ ' + str(app.date) + ' ساعت  ' + str(
        app.start_time) + ' توسط پزشک ' + action + ' شد.'
    send_mail(title, body, 'onlinefoodforyou@gmail.com', [app.patient.user.email], fail_silently=False)


def send_notif_mail(app, time):
    title = ' زمان حضور در مطب'
    body = ' با سلام \n لطفا برای نوبت خود از دکتر ' + str(app.doctor.user.user.first_name) + ' ' + str(
        app.doctor.user.user.last_name) + ' ساعت ' + time + ' در مطب حضور داشته باشید.'
    send_mail(title, body, 'onlinefoodforyou@gmail.com', [app.patient.user.email], fail_silently=False)


def send_cancel_mail(app):
    title = 'کنسل شدن وقت توسط دکتر'
    body = ' با سلام \n نوبت شما از دکتر' + str(app.doctor.user.user.first_name) + ' ' + str(
        app.doctor.user.user.last_name) + ' در تاریخ ' + str(app.date) + ' ساعت  ' + str(
        app.start_time) + ' توسط پزشک کنسل شد. '
    send_mail(title, body, 'onlinefoodforyou@gmail.com', [app.patient.user.email], fail_silently=False)


def get_doctor_weekly_plan(doctor, date):
    """
    from the date given to 7 days after that returns doctor's plan
    :param doctor: the doctor whose weekly plan is required
    :param date: the start date from which the week starts
    :return: the weekly plan of doctor
    """
    weekly_plan = []
    for i in range(7):
        delta = timedelta(i)
        week_day = date + delta
        formatted_date = Gregorian(week_day.strftime('%Y-%m-%d')).persian_string()
        day_appointments = get_doctor_day_plan(doctor=doctor, date=formatted_date)
        weekly_plan.append((formatted_date, day_appointments))

    return weekly_plan


def convert_jalali_gregorian(jalali_date):
    """
    convert jalali string date to gregorian date object
    :param jalali_date: jalali date as string
    :return: gregorian date of jalali date
    """
    year, month, day = jalali_date.split('-')
    start_day = jdatetime.date(day=int(day), year=int(year), month=int(month)).togregorian()
    return start_day
