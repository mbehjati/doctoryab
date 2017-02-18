# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from appointment.logic.appointment_time import sort_appointment_times
from appointment.logic.doctor_plan import get_doctor_day_plan
from appointment.logic.search import search_by_name_or_expertise, do_advanced_search
from appointment.models import AppointmentTime
from user.doctor_plan import get_doctor_weekly_plan, convert_jalali_gregorian
from user.doctor_plan import send_app_result_mail, send_notif_mail, send_cancel_mail
from user.forms import *
from user.forms.search import AdvancedSearchForm
from user.lib.jalali import Gregorian
from user.models import *
from user.models import Doctor
from .doctor_plan import save_doctor_free_times_in_db
from .forms.doctorplan import DoctorFreeTimes
from django.core import serializers
from django.http import JsonResponse


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
    return render(request, 'user/edit_password.html', {'form': form, 'user': user})


@login_required()
def json_password(request):
    user = request.user
    json_object = {'username': user.username, 'first_name': user.first_name}
    return JsonResponse(json_object)


# def json_password(request):
#     json_serializer = serializers.get_serializer("json")()
#     json_dict = {'name': 'soli'}
#     response = json_serializer.serialize(json_dict, ensure_ascii=False, indent=2, use_natural_keys=True)
#     return HttpResponse(response, mimetype="json")


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


def get_doctor_from_req(request):
    user = request.user.id
    user_obj = User.objects.get(pk=user)
    my_user = MyUser.objects.get(user=user_obj)
    return Doctor.objects.get(user=my_user)


def get_doctor_free_times_form_from_req(request):  # TODO: move this to logic
    form = DoctorFreeTimes()
    form.start_date = request.POST['start_date']
    form.end_date = request.POST['end_date']
    form.start_time = request.POST['start_time']
    form.end_time = request.POST['end_time']
    form.visit_duration = request.POST['visit_duration']
    return form


def doctor_plan(request):
    doctor = get_doctor_from_req(request)
    now = datetime.now()
    date = Gregorian(now.strftime('%Y-%m-%d')).persian_string()
    cancel_deadline = Gregorian(str((datetime.now() + timedelta(days=1)).date())).persian_string()
    apps = get_doctor_day_plan(date, doctor)
    today = date

    if request.method == 'POST':

        if 'app_action' in request.POST:
            app = request.POST['appointment']
            app = get_object_or_404(AppointmentTime, id=app)
            if request.POST['app_action'] == 'confirmed':
                app.confirmation = '3'
                app.save()
                x = AppointmentTime.objects.get(id=app.id)
                send_app_result_mail(app, True)
            elif request.POST['app_action'] == 'not_confirmed':
                app.confirmation = '2'
                app.save()
                new_app = AppointmentTime(date=app.date, start_time=app.start_time, end_time=app.end_time,
                                          doctor=app.doctor, duration=app.duration)
                new_app.save()
                send_app_result_mail(app, False)
            elif request.POST['app_action'] == 'delete':
                app.delete()
            elif request.POST['app_action'] == 'presence':
                app.presence = True
                app.save()
            elif request.POST['app_action'] == 'mail':
                presence_time = request.POST['presence_time']
                send_notif_mail(app, presence_time)
            elif request.POST['app_action'] == 'cancel':
                app.confirmation = '2'
                app.save()
                new_app = AppointmentTime(date=app.date, start_time=app.start_time, end_time=app.end_time,
                                          doctor=app.doctor, duration=app.duration)
                new_app.save()
                send_cancel_mail(app)

        date = request.POST.get('date')
        apps = get_doctor_day_plan(date, doctor)

    apps = None if len(apps) == 0 else apps
    return render(request, 'user/doctor_plan.html',
                  {'apps': apps, 'date': date, 'today': today, 'cancel_deadline': cancel_deadline})


def doctor_free_time(request):
    message = ''
    response = False

    if request.method == 'POST':
        doctor = get_doctor_from_req(request)
        form = get_doctor_free_times_form_from_req(request)
        if form.is_data_valid():
            save_doctor_free_times_in_db(doctor, form)
            message = 'اطلاعات شما با موفقیت ثبت شد. '  # TODO: send to django messages
            response = True
        else:
            message = '*اطلاعات واردشده مجاز نمی‌باشد. '

    return render(request, 'user/set_doctor_free_times.html', {'message': message, 'response': response})


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

    return render(request, 'appointment/advanced_search.html', {'form': form, 'result': result})


@login_required()
def user_appointments(request):
    appointments = list(
        AppointmentTime.objects.filter(patient=request.user.myuser))  # TODO: Check for another way to convert queryset
    sorted_appointments = sort_appointment_times(appointments)
    return render(request, 'user/appointments_list.html', {'appointments': sorted_appointments})


@login_required()
def doctor_weekly_plan(request):
    start_day = datetime.now()

    if request.method == 'POST':
        start_day = convert_jalali_gregorian(request.POST['date'])

    weekly_plan = get_doctor_weekly_plan(get_doctor_from_req(request), start_day)
    return render(request, 'user/weekly_plan.html', {'plan': weekly_plan})
