# -*- coding: UTF-8 -*-
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse

from appointment.logic.doctor_plan import get_doctor_day_plan
from user.forms import *
from user.lib.jalali import Gregorian
from user.models import *
from .doctor_plan import save_doctor_free_times_in_db
from .forms.doctorplan import DoctorFreeTimes


def generate_pdf(request):
    file = open('user/static/user/contract/contract.pdf', 'rb')
    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')


@login_required(login_url='/')
def view_profile(request):
    user_id = request.user.id
    print('here')
    try:
        user1 = User.objects.get(pk=user_id)
        myuser = MyUser.objects.get(user=user1)
        if not myuser.is_doctor:
            return render(request, 'user/profile_user.html', {'myuser': myuser})
        else:
            doctor = Doctor.objects.get(user=myuser)
            return render(request, 'user/profile_doctor.html', {'doctor': doctor})

    except User.DoesNotExist:
        redirect('/')


@login_required()
def edit_password(request):
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
    user = request.user
    myuser = MyUser.objects.get(user=user)
    form_user = EditUserForm(request.POST or None, initial={'first_name': myuser.user.first_name,
                                                            'last_name': myuser.user.last_name,
                                                            'email': myuser.user.email})
    form_myuser = EditMyUserForm(request.POST or None, request.FILES or None,
                                 initial={'phone_number': myuser.phone_number,
                                          'national_code': myuser.national_code,
                                          'image': myuser.image})
    # print(form_myuser.errors)
    doctor = None
    form_doctor = None
    if myuser.is_doctor:
        doctor = Doctor.objects.get(user=myuser)
        form_doctor = EditMyDoctorForm(request.POST or None, initial={'university': doctor.university,
                                                                      'year_diploma': doctor.year_diploma,
                                                                      'diploma': doctor.diploma,
                                                                      'office_address': doctor.office_address,
                                                                      'office_phone_number': doctor.office_phone_number,
                                                                      'insurance': doctor.insurance.all(),
                                                                      'expertise': doctor.expertise})
    # print(form_myuser.image)
    # print(form_user.errors)
    # print(form_doctor.errors)
    if request.method == 'POST':
        if form_user.is_valid() * form_myuser.is_valid():
            user.first_name = form_user.cleaned_data['first_name']
            user.last_name = form_user.cleaned_data['last_name']
            user.email = form_user.cleaned_data['email']
            myuser.phone_number = form_myuser.cleaned_data['phone_number']
            myuser.national_code = form_myuser.cleaned_data['national_code']
            myuser.image = form_myuser.cleaned_data['image']
            user.save()
            myuser.user = user
            myuser.save()
            if myuser.is_doctor:
                print(form_doctor.errors)
                if form_doctor.is_valid():
                    doctor.university = form_doctor.cleaned_data['university']
                    doctor.year_diploma = form_doctor.cleaned_data['year_diploma']
                    doctor.diploma = form_doctor.cleaned_data['diploma']
                    doctor.office_address = form_doctor.cleaned_data['office_address']
                    doctor.office_phone_number = form_doctor.cleaned_data['office_phone_number']
                    doctor.insurance = form_doctor.cleaned_data['insurance']
                    doctor.expertise = form_doctor.cleaned_data['expertise']
                    doctor.user = myuser
                    doctor.save()
            messages.success(request, 'مشخصات ویرایش شد.')
            return redirect('/user/edit-profile')

    return render(request, 'user/profile.html',
                  {'form_user': form_user, 'form_myuser': form_myuser, 'form_doctor': form_doctor,
                   'myuser': myuser, 'doctor': doctor})


# @login_required()
# def edit_profile(request):
#     user = request.user
#     myuser = MyUser.objects.get(user=user)
#     form_user = EditUserForm(request.POST or None, initial={'first_name': myuser.user.first_name,
#                                                             'last_name': myuser.user.last_name,
#                                                             'email': myuser.user.email})
#     form_myuser = EditMyUserForm(request.POST or None, initial={'phone_number': myuser.phone_number,
#                                                                 'national_code': myuser.national_code})
#     if not myuser.is_doctor:
#         if request.method == 'POST':
#             # form = EditProfileForm(request.POST)
#             if form_user.is_valid() * form_myuser.is_valid():
#                 user.first_name = form_user.cleaned_data['first_name']
#                 user.last_name = form_user.cleaned_data['last_name']
#                 user.email = form_user.cleaned_data['email']
#                 myuser.phone_number = form_myuser.cleaned_data['phone_number']
#                 myuser.national_code = form_myuser.cleaned_data['national_code']
#                 user.save()
#                 myuser.user = user
#                 myuser.save()
#             return HttpResponseRedirect('/user/profile')
#         return render(request, 'user/edit_profile_user.html',
#                       {'form_user': form_user, 'form_myuser': form_myuser, 'myuser': myuser})
#     else:
#         doctor = Doctor.objects.get(user=myuser)
#         form_doctor = EditMyDoctorForm(request.POST or None, initial={'university': doctor.university,
#                                                                       'year_diploma': doctor.year_diploma,
#                                                                       'diploma': doctor.diploma,
#                                                                       'office_address': doctor.office_address,
#                                                                       'office_phone_number': doctor.office_phone_number})
#         if request.method == 'POST':
#             if form_user.is_valid() * form_myuser.is_valid():
#                 user.first_name = form_user.cleaned_data['first_name']
#                 user.last_name = form_user.cleaned_data['last_name']
#                 user.email = form_user.cleaned_data['email']
#                 myuser.phone_number = form_myuser.cleaned_data['phone_number']
#                 myuser.national_code = form_myuser.cleaned_data['national_code']
#                 user.save()
#                 myuser.user = user
#                 myuser.save()
#             if form_doctor.is_valid():
#                 doctor.university = form_doctor.cleaned_data['university']
#                 doctor.year_diploma = form_doctor.cleaned_data['year_diploma']
#                 doctor.diploma = form_doctor.cleaned_data['diploma']
#                 doctor.office_address = form_doctor.cleaned_data['office_address']
#                 doctor.office_phone_number = form_doctor.cleaned_data['office_phone_number']
#                 doctor.user = myuser
#                 doctor.save()
#             return HttpResponseRedirect('/user/profile')
#         return render(request, 'user/profile.html',
#                       {'form_user': form_user, 'form_myuser': form_myuser, 'form_doctor': form_doctor,
#                        'myuser': myuser, 'doctor': doctor})


def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        upf = MyUserForm(request.POST, request.FILES, prefix='userprofile')
        df = DoctorForm(request.POST, request.FILES
                        # , request.POST, request.POST, request.POST, request.POST, request.POST,
                        # request.FILES
                        , prefix='doctorprofile'
                        )
        for err in df.errors:
            print(err)
        if uf.is_valid() * upf.is_valid():
            user = User.objects.create_user(username=uf.cleaned_data['username'], password=uf.cleaned_data['password'],
                                            first_name=uf.cleaned_data['first_name'],
                                            last_name=uf.cleaned_data['last_name'],
                                            email=uf.cleaned_data['email'])
            user.is_active = True
            user.save()
            userprofile = MyUser(user=user, phone_number=upf.cleaned_data['phone_number'],
                                 national_code=upf.cleaned_data['national_code'],
                                 image=upf.cleaned_data['image']
                                 )
            userprofile.save()
            # print('is df valid:', df.is_valid(), '\n')
            if df.is_valid():
                # print('yes df is valid')
                doctorprofile = Doctor(user=userprofile, university=df.cleaned_data['university'],
                                       year_diploma=df.cleaned_data['year_diploma'],
                                       diploma=df.cleaned_data['diploma'],
                                       office_address=df.cleaned_data['office_address'],
                                       office_phone_number=df.cleaned_data['office_phone_number'],
                                       expertise=df.cleaned_data['expertise'],
                                       contract=df.cleaned_data['contract'],
                                       insurance=df.cleaned_data['insurance']
                                       )
                # print(doctorprofile.year_diploma)
                userprofile.is_doctor = True
                userprofile.save()
                # print(userprofile.is_doctor)
                doctorprofile.save()
            new_user = authenticate(username=uf.cleaned_data['username'], password=uf.cleaned_data['password'])
            django_login(request, new_user)
            messages.success(request, 'شما با موفقیت ثبت نام شدید.')
            return redirect('/user/edit-profile')
    else:
        uf = UserForm(prefix='user')
        upf = MyUserForm(prefix='userprofile')
        df = DoctorForm(prefix='doctorprofile')
    return render(request, 'user/register_user.html', {'userform': uf, 'userprofileform': upf, 'doctorprofile': df})


# def login(request):
#     message = ''
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 findeduser = User.objects.get(pk=user.id)
#                 my_user = MyUser.objects.get(user=findeduser)
#
#                 if findeduser.is_active:
#                     if Doctor.objects.filter(user=my_user).count() > 0:
#                         doc = Doctor.objects.get(user=my_user)
#                         django_login(request, user)
#                     else:
#                         django_login(request, user)
#                     return redirect('/user/')
#                 else:
#                     form = LoginForm()
#                     # raise forms.ValidationError('.حساب کاربری شما غیرفعال است.')
#                     message = '.حساب کاربری شما غیرفعال است.'
#             else:
#                 form = LoginForm()
#                 # print('pass or username wrong')
#                 # raise forms.ValidationError('نام کاربری یا گذرواژه شما اشتباه است..')
#                 message = 'نام کاربری یا گذرواژه شما اشتباه است.'
#     else:
#         form = LoginForm()
#     return render(request, 'user/login_user.html', {'form': form, 'message': message})


def logout(request):
    django_logout(request)
    # return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')


def login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            findeduser = User.objects.get(pk=user.id)
            my_user = MyUser.objects.get(user=findeduser)
            if findeduser.is_active:
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


def get_doctor_free_times_form_from_req(request):
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
    apps = get_doctor_day_plan(date, doctor)

    if request.method == 'POST':
        date = request.POST['date']
        apps = get_doctor_day_plan(date, doctor)

    apps = None if len(apps) == 0 else apps
    return render(request, 'user/doctor_plan.html', {'apps': apps, 'date': date})


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

    return render(request, 'user/set_doctor_free_times.html', {'message': message, 'response': response})
