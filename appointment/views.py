# -*- coding: UTF-8 -*-
import json
from datetime import datetime

import jdatetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from appointment.forms import AdvancedSearchForm
from appointment.logic.doctor_plan import get_doctor_all_plan, send_app_reserve_mail
from appointment.logic.search import do_advanced_search, search_by_name_or_expertise
from appointment.models import AppointmentTime
from appointment.serializers import DateAppointmentSerializer
from user.models import MyUser, Doctor
from user.serializers import DoctorSerializer


def home(request):
    return render(request, 'index.html')


def get_doctor_from_req(request):
    user = request.user.id
    user_obj = User.objects.get(pk=user)
    my_user = MyUser.objects.get(user=user_obj)
    return Doctor.objects.get(user=my_user)


def doctor_detail(request, doctor_id):
    return render(request, 'appointment/doctor_detail.html')


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor_serializer = DoctorSerializer(doctor)
    return Response(doctor_serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_appointments(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    now = datetime.now()
    date = jdatetime.date.fromgregorian(date=now).strftime('%Y-%m-%d')
    apps = get_doctor_all_plan(date, doctor)
    date_appointment_serializer = DateAppointmentSerializer(apps, many=True)
    return Response(date_appointment_serializer.data)


@api_view(['POST'])
def reserve_appointment(request):
    app_id = request.POST['appointment']
    appointment = get_object_or_404(AppointmentTime, id=app_id)
    appointment.patient = request.user.myuser
    appointment.save()
    messages.success(request, 'نوبت شما با موفقیت رزرو گردید')
    send_app_reserve_mail(appointment)
    return HttpResponse(json.dumps('success'))
    # TODO return what??


def search(request):
    result = None
    form = AdvancedSearchForm()

    if request.method == 'POST':
        if 'keyword' in request.POST:
            form, result = simple_search(request)
        else:
            form = AdvancedSearchForm(request.POST)
            result = do_advanced_search(form)

    return render(request, 'appointment/advanced_search.html', {'form': form, 'result': result})


def simple_search(request):
    keyword = request.POST['keyword']
    result = search_by_name_or_expertise(Doctor.objects.all(), keyword)
    form = AdvancedSearchForm(initial={'name': keyword})
    return form, result


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def search_keyword(request):
    keyword = request.POST['keyword']
    result = search_by_name_or_expertise(Doctor.objects.all(), keyword)
    result_serializer = DoctorSerializer(result, many=True)
    return Response(result_serializer.data)
