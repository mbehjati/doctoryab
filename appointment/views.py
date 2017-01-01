# Create your views here.
# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta

from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render

from user.forms import LoginForm
from .forms import DoctorFreeTimes, AdvancedSearchForm
from .models import *


def home(request):
    message = ''
    if request.method == "POST":
        message = login(request)
    return render(request, 'index.html', {'form': LoginForm(), 'message': message})


def login(request):
    message = ''
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
                # return redirect('/user/')
                return "کاربر عزیز خوش آمدید."
            else:
                form = LoginForm()
                # raise forms.ValidationError('.حساب کاربری شما غیرفعال است.')
                message = ".حساب کاربری شما غیرفعال است."
        else:
            form = LoginForm()
            # print("pass or username wrong")
            # raise forms.ValidationError('نام کاربری یا گذرواژه شما اشتباه است..')
            message = "نام کاربری یا گذرواژه شما اشتباه است."
    return message


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
    if minute >= 60:
        minute %= 60
        hour = (hour + 1) % 12
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


def doctor_free_time(request):
    message = ''
    response = False

    if request.method == 'POST':
        doctor = get_doctor_from_req(request)
        form = DoctorFreeTimes()
        form.start_date = request.POST['start_date']
        form.end_date = request.POST['end_date']
        form.start_time = request.POST['start_time']
        form.end_time = request.POST['end_time']
        form.visit_duration = request.POST['visit_duration']
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


def do_advanced_search(form):
    if form.is_valid():
        doctors = search_by_name(Doctor.objects.all(), form.cleaned_data['name'])
        doctors = search_by_expertise(doctors, form.cleaned_data['expertise'])
        doctors = search_by_date(doctors, form.cleaned_data['date'], AppointmentTime.objects.all())
        doctors = search_by_address(doctors, form.cleaned_data['address'])
        doctors = search_by_insurance(doctors, form.cleaned_data['insurance'])
        return doctors


def search_by_name(doctors, name):
    ans = []
    for doc in doctors:
        if name.replace(' ', '') in (doc.user.user.first_name + doc.user.user.last_name).replace(' ', ''):
            ans.append(doc)
    return ans


def search_by_expertise(doctors, expertise):
    ans = []
    if expertise == 'همه':
        return doctors
    for doc in doctors:
        if doc.expertise.name == expertise:
            ans.append(doc)
    return ans


def search_by_date(doctors, date, app_times):
    ans = []
    if date == '':
        return doctors
    for app_time in app_times:
        if app_time.date == date and app_time.doctor not in ans and app_time.doctor in doctors:
            ans.append(app_time.doctor)
    return ans


def search_by_address(doctors, address):
    ans = []
    for doc in doctors:
        if address in doc.office_address:
            ans.append(doc)
    return ans


def search_by_insurance(doctors, insurance):
    if insurance == 'همه':
        return doctors
    ans = []
    for doc in doctors:
        for ins in doc.insurance.all():
            if ins.name == insurance:
                ans.append(doc)
    return ans
