from datetime import datetime, timedelta

from django.core.mail import send_mail

from appointment.logic.appointment_time import is_time_before, add_time
from appointment.models import AppointmentTime


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
