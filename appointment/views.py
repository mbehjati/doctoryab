# Create your views here.
# -*- coding: UTF-8 -*-
from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import render

from appointment.logic.doctor_plan import save_doctor_free_times_in_db, get_doctor_day_plan
from appointment.logic.search import do_advanced_search
from .forms import DoctorFreeTimes, AdvancedSearchForm
from .jalali import Gregorian
from .models import *


def home(request):
    return render(request, 'index.html', {})


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
    now = datetime.now()
    date = Gregorian(now.strftime("%Y-%m-%d")).persian_string()
    if request.method == 'POST':
        date = request.POST['date']
        doctor = get_doctor_from_req(request)
        apps = get_doctor_day_plan(date, doctor)
        apps = None if len(apps) == 0 else apps

    return render(request, 'appointment/doctor_plan.html', {'apps': apps, 'date': date})


