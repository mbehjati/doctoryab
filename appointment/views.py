# Create your views here.
# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from appointment.search import do_advanced_search
from user.forms import LoginForm
from .forms import DoctorFreeTimes, AdvancedSearchForm
from .models import *


def home(request):
    message = ''
    if request.method == "POST":
        message = login(request)
    return render(request, 'index.html', {})  # , {'form': LoginForm(), 'message': message})


def login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            findeduser = User.objects.get(pk=user.id)
            my_user = MyUser.objects.get(user=findeduser)
            if findeduser.is_active:
                django_login(request, user)
                messages.success(request, 'کاربر عزیز خوش آمدید.')
        else:
            messages.warning(request, 'نام کاربری یا گذرواژه شما اشتباه است.')

    return redirect(request.META.get('HTTP_REFERER'))


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


def is_time_before(first, second):
    if 'pm' in first and 'am' in second:
        return False
    if 'am' in first and 'pm' in second:
        return True
    if '12:' in first and '12:' not in second:
        return True
    if first > second:
        return False
    return True


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


def add_time(start_time, duration):
    duration = int(duration)
    hour = int(start_time.split(':')[0])
    minute = int(start_time.split(':')[1][0:len(start_time.split(':')[1]) - 2])
    postfix = start_time[len(start_time) - 2:len(start_time)]

    minute += duration
    hour = (hour + 1) % 12 if minute >= 60 else hour
    minute %= 60
    if hour == 0:
        hour = 12
        postfix = 'pm'

    return str(hour) + ':' + str(minute).zfill(2) + postfix


def calc_visit_times_for_a_day(doctor, day, start_time, end_time, duration):
    ans = []
    while is_time_before(add_time(start_time, duration), end_time):
        ans.append(
            AppointmentTime(date=day, start_time=start_time, end_time=add_time(start_time, duration), duration=duration,
                            doctor=doctor))
        start_time = add_time(start_time, duration)
    return ans


def get_doctor_from_req(request):
    user = request.user.id
    user_obj = User.objects.get(pk=user)
    my_user = MyUser.objects.get(user=user_obj)
    return Doctor.objects.get(user=my_user)


def get_doctor_free_times_form_from_req(request):
    form = DoctorFreeTimes()
    form.start_date = request.POST['start_date']
    form.end_date = request.POST['end_date']
    form.start_time = request.POST['start_time']
    form.end_time = request.POST['end_time']
    form.visit_duration = request.POST['visit_duration']
    return form


def doctor_free_time(request):
    message = ''
    response = False

    if request.method == 'POST':
        doctor = get_doctor_from_req(request)
        form = get_doctor_free_times_form_from_req(request)
        if form.is_data_valid():
            save_doctor_free_times_in_db(doctor, form)
            message = 'اطلاعات شما با موفقیت ثبت شد. '
            response = True
        else:
            message = '*اطلاعات واردشده مجاز نمی‌باشد. '

    return render(request, 'appointment/set_doctor_free_times.html', {'message': message, 'response': response})


def search(request):
    form = AdvancedSearchForm()
    result = None
    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST)
        result = do_advanced_search(form)
    return render(request, 'appointment/advanced-search.html', {'form': form, 'result': result})


def doctor_plan(request):
    apps = None
    date = ''
    if request.method == 'POST':
        date = request.POST['date']
        doctor = get_doctor_from_req(request)
        apps = get_doctor_day_plan(date, doctor)
        apps = None if len(apps) == 0 else apps

    return render(request, 'appointment/doctor_plan.html', {'apps': apps, 'date': date})


def sort_appointment_times(apps):
    for i in range(len(apps)):
        for j in range(len(apps)):
            if is_time_before(apps[i].start_time, apps[j].start_time):
                apps[i], apps[j] = apps[j], apps[i]
    print(apps)
    return apps


def get_doctor_day_plan(date, doctor):
    return sort_appointment_times(list(AppointmentTime.objects.filter(doctor=doctor, date=date)))
