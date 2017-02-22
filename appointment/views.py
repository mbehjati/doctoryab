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
        data = [
            {
                "user": {
                    "id": 2,
                    "phone_number": "09196855227",
                    "national_code": "0440482022",
                    "image": None,
                    "is_doctor": True,
                    "user": {
                        "id": 3,
                        "password": "pbkdf2_sha256$24000$VkqsUA7T9TdE$1HlY27ENDRctcuXLudwPzSYXXH3FTItk9JU7qcrxEKQ=",
                        "last_login": "2017-02-22T13:59:24.600709Z",
                        "is_superuser": False,
                        "username": "doci",
                        "first_name": "علی",
                        "last_name": "بهجتی",
                        "email": "bahjatia@gmail.com",
                        "is_staff": False,
                        "is_active": True,
                        "date_joined": "2017-02-16T08:02:59.026157Z",
                        "groups": [],
                        "user_permissions": []
                    }
                },
                "diploma": "تخصص",
                "lat_location": "1",
                "lon_location": "1",
                "office_address": "قیطریه- خ روشنایی",
                "office_phone_number": "02122670861",
                "expertise": {
                    "name": "چشم"
                },
                "insurance": [
                    {
                        "name": "البرز"
                    }
                ],
                "title": "متخصص"
            },
            {
                "user": {
                    "id": 3,
                    "phone_number": "09888888888",
                    "national_code": "0440482021",
                    "image": None,
                    "is_doctor": True,
                    "user": {
                        "id": 4,
                        "password": "pbkdf2_sha256$24000$QrQnJSC6U8lK$A+c8SEAx//79fKbnpQAKpGZahVOY9UeUpX54GBnkfKo=",
                        "last_login": "2017-02-22T17:27:10.929667Z",
                        "is_superuser": False,
                        "username": "doctor",
                        "first_name": "مونا",
                        "last_name": "ایزدی",
                        "email": "melikabehjati@gmail.com",
                        "is_staff": False,
                        "is_active": True,
                        "date_joined": "2017-02-20T21:17:14.866544Z",
                        "groups": [],
                        "user_permissions": []
                    }
                },
                "diploma": "تخصص",
                "lat_location": "35",
                "lon_location": "51",
                "office_address": "تهران- بلوار اندرزگو",
                "office_phone_number": "02188888888",
                "expertise": {
                    "name": "چشم"
                },
                "insurance": [
                    {
                        "name": "البرز"
                    },
                    {
                        "name": "ایران"
                    }
                ],
                "title": "متخصص"
            }
        ]
    return render(request, 'appointment/searchby_location.html', {'my_data': data, 'doctors': doctors})
