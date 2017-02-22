# -*- coding: UTF-8 -*-
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from appointment.logic.doctor_plan import get_doctor_all_plan, send_app_reserve_mail
from user.lib.jalali import Gregorian
from .models import *


def home(request):
    return render(request, 'index.html')


def get_doctor_from_req(request):
    user = request.user.id
    user_obj = User.objects.get(pk=user)
    my_user = MyUser.objects.get(user=user_obj)
    return Doctor.objects.get(user=my_user)


def doctor_detail(request, doctor_id):
    if request.method == 'POST':
        app_id = request.POST['appointment']
        appointment = get_object_or_404(AppointmentTime, id=app_id)
        appointment.patient = request.user.myuser
        appointment.save()
        messages.success(request, 'نوبت شما با موفقیت رزرو گردید')
        send_app_reserve_mail(appointment)
    doctor = get_object_or_404(Doctor, id=doctor_id)
    now = datetime.now()
    date = Gregorian(now.strftime("%Y-%m-%d")).persian_string()
    apps = get_doctor_all_plan(date, doctor)

    return render(request, 'appointment/doctor_detail.html', {'doctor': doctor, 'apps': apps})


def search_by_location(request):
    doctors = Doctor.objects.order_by('lat_location', 'lon_location')
    for doc in doctors:
        print(doc.user.user.username, doc.lat_location)
    return render(request, 'appointment/searchby_location.html', {'doctors': doctors})
