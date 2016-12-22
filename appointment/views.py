# Create your views here.
from datetime import datetime, timedelta

from django.shortcuts import render

from .forms import DoctorFreeTimes
from .models import *


def home(request):
    return render(request, 'index.html')


def save_doctor_free_times(form):
    start_date = datetime.strptime(form.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(form.end_date, '%Y-%m-%d')
    day = timedelta(days=1)

    while start_date <= end_date:
        save_visit_times_for_a_day(start_date, form.start_time, form.end_time, form.visit_duration)
        start_date = start_date + day


def is_time_before(first, second):
    if 'pm' in first and 'am' in second:
        return False
    if 'am' in first and 'pm' in second:
        return True
    if '12:' in first and '12:' not in second:
        return True
    if first >= second:
        return False
    return True


def add_appointment_time(doctor, day, start_time, duration):
    appointment_time = AppointmentTime(date=day, start_time=start_time, duration=duration, doctor=doctor)
    appointment_time.save()


def add_time(start_time, duration):
    hour = int(start_time.split(':')[0])
    minute = int(start_time.split(':')[1][0:len(start_time.split(':')[1]) - 2])
    postfix = start_time[len(start_time)-2:len(start_time)]
    minute += duration
    if minute >= 60:
        minute %= 60
        hour = (hour + 1) % 12
    if hour == 0 :
        hour = 12
        postfix = 'pm'
    return str(hour) + ':' + str(minute).zfill(2) + postfix


def save_visit_times_for_a_day(day, start_time, end_time, duration):
    if not is_time_before(add_time(start_time, duration), end_time):
        return
    while is_time_before(start_time, end_time):
        add_appointment_time(day, start_time, duration)
        start_time = add_time(start_time, duration)


def doctor_free_time(request):
    message = ''
    response = False
    if request.method == 'POST':
        form = DoctorFreeTimes()
        form.start_date = request.POST['start_date']
        form.end_date = request.POST['end_date']
        form.start_time = request.POST['start_time']
        form.end_time = request.POST['end_time']
        form.visit_duration = request.POST['visit_duration']
        if form.is_data_valid():
            save_doctor_free_times(form)
            message = 'اطلاعات شما با موفقیت ثبت شد. '
            response = True
        else:
            message = '*اطلاعات واردشده مجاز نمی‌باشد. '

    return render(request, 'appointment/set_doctor_free_times.html', {'message': message, 'response': response})
