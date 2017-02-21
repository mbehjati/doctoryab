# -*- coding: UTF-8 -*-
import json
from datetime import datetime

import jdatetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from appointment.logic.doctor_plan import get_doctor_all_plan, send_app_reserve_mail
from .models import *
from .serializers import AppointmentSerializer


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
    date = jdatetime.date.fromgregorian(date=now).strftime('%Y-%m-%d')
    apps = get_doctor_all_plan(date, doctor)

    return render(request, 'appointment/doctor_detail.html', {'doctor': doctor, 'apps': apps})


@api_view(['GET'])
def get_appointments(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    now = datetime.now()
    date = jdatetime.date.fromgregorian(date=now).strftime('%Y-%m-%d')
    apps = get_doctor_all_plan(date, doctor)
    res = {}
    for i in range(len(apps)):
        res[apps[i]['date']] = []
        for j in range(len(apps[i]['apps'])):
            # apps[i]['apps'][j] = serializers.serialize('json', [apps[i]['apps'][j], ])
            res[apps[i]['date']].append(AppointmentSerializer(apps[i]['apps'][j]).data)
            print(res)
    return Response(res)
    # return HttpResponse(json.dumps(apps))


def reserve_appointment(request, app_id):
    appointment = get_object_or_404(AppointmentTime, id=app_id)
    appointment.patient = request.user.myuser
    appointment.save()
    messages.success(request, 'نوبت شما با موفقیت رزرو گردید')
    send_app_reserve_mail(appointment)
    return HttpResponse(json.dumps('success'))
    # TODO return what??
