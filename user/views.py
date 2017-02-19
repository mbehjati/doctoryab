# -*- coding: UTF-8 -*-
import json
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from appointment.logic.appointment_time import sort_appointment_times
from appointment.logic.doctor_plan import get_doctor_day_plan
from appointment.logic.search import search_by_name_or_expertise, do_advanced_search
from appointment.models import AppointmentTime
from appointment.serializers import AppointmentSerializer
from user.doctor_plan import get_doctor_weekly_plan, convert_jalali_gregorian, app_confirmation_action, \
    delete_free_app_action, send_presence_mail_action, cancel_app_action, set_presence_action, \
    app_not_confirmation_action, get_doctor_free_times_form_from_req, get_doctor_from_req, get_app_from_req
from user.forms import *
from user.forms.search import AdvancedSearchForm
from user.lib.jalali import Gregorian
from user.models import *
from user.models import Doctor
from .doctor_plan import save_doctor_free_times_in_db
from .serializers import DoctorSerializer


def upload_contract_file(request):
    """ uploads primary contract file to site which user can download and fill it """
    file = open('user/static/user/contract/contract.pdf', 'rb')
    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')


@login_required()
def edit_password(request):
    """ user can his/her password

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
    return render(request, 'user/edit_password.html', {'form': form, 'user': user})


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
    user_form = EditUserForm(request.POST or None, initial={'first_name': my_user.user.first_name,
                                                            'last_name': my_user.user.last_name,
                                                            'email': my_user.user.email})
    my_user_form = EditMyUserForm(request.POST or None, request.FILES or None,
                                  initial={'phone_number': my_user.phone_number,
                                           'national_code': my_user.national_code})
    # first set doctor  model and form to None then
    doctor = None
    doctor_form = None
    # decides based on my_user is doctor or not to make doctor model and form or not
    if my_user.is_doctor:
        doctor = Doctor.objects.get(user=my_user)
        doctor_form = EditMyDoctorForm(request.POST or None, initial={'university': doctor.university,
                                                                      'year_diploma': doctor.year_diploma,
                                                                      'diploma': doctor.diploma,
                                                                      'office_address': doctor.office_address,
                                                                      'office_phone_number': doctor.office_phone_number,
                                                                      'insurance': doctor.insurance.all(),
                                                                      'expertise': doctor.expertise})

    if request.method == 'POST':
        # if method is post sets user info
        if user_form.is_valid() and my_user_form.is_valid():
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            my_user.phone_number = my_user_form.cleaned_data['phone_number']
            my_user.national_code = my_user_form.cleaned_data['national_code']
            if not (my_user_form.cleaned_data['image'] is None):
                my_user.image = my_user_form.cleaned_data['image']
            user.save()
            my_user.user = user
            my_user.save()
            if my_user.is_doctor:
                if doctor_form.is_valid():
                    doctor.university = doctor_form.cleaned_data['university']
                    doctor.year_diploma = doctor_form.cleaned_data['year_diploma']
                    doctor.diploma = doctor_form.cleaned_data['diploma']
                    doctor.office_address = doctor_form.cleaned_data['office_address']
                    doctor.office_phone_number = doctor_form.cleaned_data['office_phone_number']
                    doctor.insurance = doctor_form.cleaned_data['insurance']
                    doctor.expertise = doctor_form.cleaned_data['expertise']
                    doctor.user = my_user
                    doctor.save()
            messages.success(request, 'مشخصات ویرایش شد.')
            return redirect('/user/edit-profile')

    return render(request, 'user/profile.html',
                  {'user_form': user_form, 'my_user_form': my_user_form, 'doctor_form': doctor_form,
                   'my_user': my_user, 'doctor': doctor})


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, prefix='user')
        my_user_form = MyUserForm(request.POST, request.FILES, prefix='my_user')
        doctor_form = DoctorForm(request.POST, request.FILES,
                                 prefix='doctor')
        if user_form.is_valid() and my_user_form.is_valid():
            # if user fill the forms right, so he is user and user, MyUser models will be made
            user = User.objects.create_user(username=user_form.cleaned_data['username'],
                                            password=user_form.cleaned_data['password'],
                                            first_name=user_form.cleaned_data['first_name'],
                                            last_name=user_form.cleaned_data['last_name'],
                                            email=user_form.cleaned_data['email'])
            user.is_active = True
            user.save()
            my_user = MyUser(user=user, phone_number=my_user_form.cleaned_data['phone_number'],
                             national_code=my_user_form.cleaned_data['national_code'],
                             image=my_user_form.cleaned_data['image'])
            my_user.save()
            if doctor_form.is_valid():
                # so user is doctor, creates Doctor model and save it, also set is_doctor of my_user to true
                doctor = Doctor(user=my_user, university=doctor_form.cleaned_data['university'],
                                year_diploma=doctor_form.cleaned_data['year_diploma'],
                                diploma=doctor_form.cleaned_data['diploma'],
                                office_address=doctor_form.cleaned_data['office_address'],
                                office_phone_number=doctor_form.cleaned_data['office_phone_number'],
                                expertise=doctor_form.cleaned_data['expertise'],
                                contract=doctor_form.cleaned_data['contract'])
                doctor.save()
                for ins in doctor_form.cleaned_data['insurance']:
                    doctor.insurance.add(ins)
                my_user.is_doctor = True
                my_user.save()

            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'])
            django_login(request, new_user)
            messages.success(request, 'شما با موفقیت ثبت نام شدید.')
            return redirect('/user/edit-profile')
    else:
        user_form = UserForm(prefix='user')
        my_user_form = MyUserForm(prefix='my_user')
        doctor_form = DoctorForm(prefix='doctor')
    return render(request, 'user/register_user.html',
                  {'user_form': user_form, 'my_user_form': my_user_form, 'doctor_form': doctor_form})


def logout(request):
    django_logout(request)
    return redirect('/')


def login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            finded_user = User.objects.get(pk=user.id)
            if finded_user.is_active:
                django_login(request, user)
                messages.success(request, 'کاربر عزیز خوش آمدید.')
        else:
            messages.warning(request, 'نام کاربری یا گذرواژه شما اشتباه است.')

    return redirect(request.META.get('HTTP_REFERER'))


def doctor_plan(request):
    doctor = get_doctor_from_req(request)
    today = date = Gregorian(datetime.now().strftime('%Y-%m-%d')).persian_string()
    cancel_deadline = Gregorian(str((datetime.now() + timedelta(days=1)).date())).persian_string()

    if 'date' in request.session:
        date = request.session['date']
        del request.session['date']
    apps = get_doctor_day_plan(date, doctor)

    if request.method == 'POST':
        date = request.POST.get('date')
        apps = get_doctor_day_plan(date, doctor)

    apps = None if len(apps) == 0 else apps

    return render(request, 'user/doctor_plan.html',
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

    return render(request, 'user/set_doctor_free_times.html', {'success': success})


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
    print('done!!!')
    return HttpResponse(json.dumps(success), content_type='application/json')


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
    # s = SearchFormSerializer()
    # print(s.data)
    return form, result


@login_required()
def user_appointments(request):
    return render(request, 'user/appointments_list.html')


@api_view(['GET'])
def get_appointments(request):
    appointments = list(
        AppointmentTime.objects.filter(patient=request.user.myuser))  # TODO: Check for another way to convert queryset
    sorted_appointments = sort_appointment_times(appointments)
    serializer = AppointmentSerializer(sorted_appointments, many=True)
    return Response(serializer.data)


@login_required()
def doctor_weekly_plan(request):
    start_day = datetime.now()

    if request.method == 'POST':
        start_day = convert_jalali_gregorian(request.POST['date'])

    weekly_plan = get_doctor_weekly_plan(get_doctor_from_req(request), start_day)
    return render(request, 'user/weekly_plan.html', {'plan': weekly_plan})


@api_view(['GET', 'POST'])
def get_doctor_weekly(request):
    start_day = datetime.now()

    if request.method == 'POST':
        start_day = convert_jalali_gregorian(request.POST['date'])

    weekly_plan = get_doctor_weekly_plan(get_doctor_from_req(request), start_day)
    w = {}
    for k, v in weekly_plan:
        w[k] = AppointmentSerializer(v, many=True).data
    return Response(w)


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


@csrf_exempt
def test(request):
    print('hello')
    print(request.POST['data'])
    return HttpResponse(json.dumps('done!!'), content_type='application/json')
