# -*- coding: UTF-8 -*-
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from appointment.logic.doctor_plan import get_doctor_all_plan
from appointment.logic.search import do_advanced_search, search_by_name_or_expertise
from user.lib.jalali import Gregorian
from .forms import AdvancedSearchForm
from .models import *


def home(request):
    return render(request, 'index.html')


def get_doctor_from_req(request):
    user = request.user.id
    user_obj = User.objects.get(pk=user)
    my_user = MyUser.objects.get(user=user_obj)
    return Doctor.objects.get(user=my_user)


def search(request):
    result = None
    form = AdvancedSearchForm()

    if request.method == 'POST':
        if 'keyword' in request.POST:
            keyword = request.POST['keyword']
            result = search_by_name_or_expertise(Doctor.objects.all(), keyword)
            form = AdvancedSearchForm(initial={'name': keyword})
        else:
            form = AdvancedSearchForm(request.POST)
            result = do_advanced_search(form)

    return render(request, 'appointment/advanced-search.html', {'form': form, 'result': result})


def doctor_detail(request, doctor_id):
    if request.method == 'POST':
        app_id = request.POST['appointment']
        appointment = get_object_or_404(AppointmentTime, id=app_id)
        appointment.patient = request.user.myuser
        appointment.save()
        messages.success(request, 'نوبت شما با موفقیت ثبت گردید')
    doctor = get_object_or_404(Doctor, id=doctor_id)
    now = datetime.now()
    date = Gregorian(now.strftime("%Y-%m-%d")).persian_string()
    apps = get_doctor_all_plan(date, doctor)

    return render(request, 'appointment/doctor_detail.html', {'doctor': doctor, 'apps': apps})
