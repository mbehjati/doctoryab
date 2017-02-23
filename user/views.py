# -*- coding: UTF-8 -*-
import json
from datetime import datetime, timedelta

import jdatetime
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from appointment.logic.appointment_time import sort_appointment_times
from appointment.logic.doctor_plan import get_doctor_day_plan
from appointment.models import AppointmentTime
from appointment.serializers import AppointmentSerializer, DateAppointmentSerializer
from user.doctor_plan import get_doctor_weekly_plan, convert_jalali_gregorian, app_confirmation_action, \
    delete_free_app_action, send_presence_mail_action, cancel_app_action, set_presence_action, \
    app_not_confirmation_action, get_doctor_free_times_form_from_req, get_doctor_from_req, get_app_from_req, \
    save_doctor_free_times_in_db
from user.forms import *
from user.models import *
from user.models import Doctor
from user.serializers import DoctorSerializer


def upload_contract_file(request):
    """ uploads primary contract file to site which user can download and fill it """
    file = open('user/static/user/contract/contract.pdf', 'rb')
    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')


@login_required()
def edit_password(request):
    """ user can change his/her password

         restrictions:
         just for logged in users
    """
    user = request.user
    form = EditPasswordForm(request.POST or None, username=user.username)
    if request.method == 'POST':
        if form.is_valid():
            user.set_password(form.cleaned_data['new_pass'])
            user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'رمز شما با موفقیت تغییر یافت.')
            return redirect('/user/edit-profile')
    return render(request, 'user/edit_password.html', {'form': form})


@login_required()
def edit_profile(request):
    """ user can see his/her profile information and change them if wants

     restrictions:
     just for logged in users

     passes user/my_user_doctor forms and models to register_user.html
     doctor form and model are None if user is not doctor
     """
    user = request.user
    my_user = MyUser.objects.get(user=user)
    user_form = UserForm(request.POST or None, request.FILES or None, instance=my_user,
                         for_edit_profile=True)
    # first set doctor  model and form to None then
    doctor = None
    doctor_form = None
    # decides based on my_user is doctor or not to make doctor model and form or not
    if my_user.is_doctor:
        doctor = Doctor.objects.get(user=my_user)
        doctor_form = DoctorForm(request.POST or None, instance=doctor,
                                 for_edit_profile=True)

    if request.method == 'POST':
        # if method is post sets user info
        if user_form.is_valid():
            my_user = user_form.save(user=user)
            if my_user.is_doctor:
                if doctor_form.is_valid():
                    doctor = doctor_form.save(user=my_user)
            messages.success(request, 'مشخصات ویرایش شد.')
            return redirect('/user/edit-profile')

    return render(request, 'user/profile.html',
                  {'user_form': user_form,
                   'doctor_form': doctor_form,
                   'my_user': my_user, 'doctor': doctor})


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, for_register=True)
        doctor_form = DoctorForm(request.POST, request.FILES,
                                 prefix='doctor', for_register=True)
        if user_form.is_valid():
            user = user_form.save()

            if doctor_form.is_valid():
                # so user is doctor, creates Doctor model and save it, also set is_doctor of my_user to true
                doctor = doctor_form.save(user=user)
                user.is_doctor = True
                user.save()

            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'])
            django_login(request, new_user)
            messages.success(request, 'شما با موفقیت ثبت نام شدید.')
            return redirect('/user/edit-profile')
    else:
        user_form = UserForm()
        doctor_form = DoctorForm(prefix='doctor')
    return render(request, 'user/register_user.html',
                  {'user_form': user_form,
                   'doctor_form': doctor_form})


def save_user_register_info():
    """user creation with user registration form info
        input:

    :return:
    """


def logout(request):
    django_logout(request)
    return redirect('/')


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    data = request.POST
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        finded_user = User.objects.get(pk=user.id)
        if finded_user.is_active:
            django_login(request, user)
            message = 'کاربر عزیز خوش آمدید.'
    else:
        message = 'نام کاربری یا گذرواژه شما اشتباه است.'

    return Response({'message': message})


def doctor_plan(request):
    doctor = get_doctor_from_req(request)
    today = date = jdatetime.date.fromgregorian(date=datetime.now()).strftime('%Y-%m-%d')
    cancel_deadline = jdatetime.date.fromgregorian(date=(datetime.now() + timedelta(days=1))).strftime('%Y-%m-%d')

    if 'date' in request.session:
        date = request.session['date']
        del request.session['date']
    apps = get_doctor_day_plan(date, doctor)

    if request.method == 'POST':
        date = request.POST.get('date')
        apps = get_doctor_day_plan(date, doctor)

    apps = None if len(apps) == 0 else apps

    return render(request, 'user/daily_plan.html',
                  {'apps': apps, 'date': date, 'today': today, 'cancel_deadline': cancel_deadline})


def app_action(request, action):
    app = get_app_from_req(request)
    action(app, request)
    request.session['date'] = request.POST.get('date')
    return redirect('/user/plan')


def doctor_free_time(request):
    success = 'no message'

    # if request.method == 'POST':
    #     doctor = get_doctor_from_req(request)
    #     form = get_doctor_free_times_form_from_req(request)
    #     if form.is_data_valid():
    #         save_doctor_free_times_in_db(doctor, form)
    #         success = True
    #     else:
    #         success = False

    return render(request, 'user/enter_plan.html', {'success': success})


def save_doctor_free_times(request):
    form = get_doctor_free_times_form_from_req(request)

    doctor = get_doctor_from_req(request)
    if form.is_data_valid():
        save_doctor_free_times_in_db(doctor, form)
        messages.success(request, 'اطلاعات شما با موفقیت ثبت شد.')
        success = True
    else:
        messages.success(request, '*اطلاعات وارد شده صحیح نمی‌باشد.')
        success = False
    print('done!!!', success)
    return HttpResponse(json.dumps(success), content_type='application/json')


@login_required()
def user_appointments(request):
    return render(request, 'user/appointments_list.html')


@api_view(['GET'])
def get_appointments(request):
    appointments = list(
        AppointmentTime.objects.filter(patient=request.user.myuser))  # TODO: Check for another way to convert queryset
    sorted_appointments = sort_appointment_times(appointments)
    appointments_serializer = AppointmentSerializer(sorted_appointments, many=True)
    return Response(appointments_serializer.data)


@login_required()
def doctor_weekly_plan(request):
    return render(request, 'user/weekly_plan.html')


@api_view(['GET', 'POST'])
@ensure_csrf_cookie
def get_doctor_weekly(request):
    start_day = datetime.now()

    if request.method == 'POST':
        print(request.POST)
        print(request.POST['date'])
        start_day = convert_jalali_gregorian(request.POST['date'])

    weekly_plan = get_doctor_weekly_plan(get_doctor_from_req(request), start_day)
    weekly_plan_serializer = DateAppointmentSerializer(weekly_plan, many=True)
    return Response(weekly_plan_serializer.data)


def app_confirmation(request):
    return app_action(request, app_confirmation_action)


def delete_free_app(request):
    return app_action(request, delete_free_app_action)


def send_presence_mail(request):
    return app_action(request, send_presence_mail_action)


def cancel_app(request):
    return app_action(request, cancel_app_action)


def set_presence(request):
    return app_action(request, set_presence_action)


def app_not_confirmation(request):
    return app_action(request, app_not_confirmation_action)


@api_view(['GET'])
def get_doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    serializer = DoctorSerializer(doctor)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_all_doctors(request):
    return Response(DoctorSerializer(Doctor.objects.all(), many=True).data)
