# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta

from appointment.logic.appointment_time import is_time_before, add_time, sort_appointment_times
from appointment.models import AppointmentTime


def save_doctor_free_times_in_db(doctor, form):
    for obj in calc_doctor_free_times(doctor, form):
        if not has_appointment_conflict(obj, AppointmentTime.objects.all()):
            obj.save()


def calc_doctor_free_times(doctor, form):
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


def get_doctor_day_plan(date, doctor):
    return sort_appointment_times(list(AppointmentTime.objects.filter(doctor=doctor, date=date)))
