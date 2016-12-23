# -*- coding: UTF-8 -*-
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect

from user.forms import UserForm, MyUserForm, DoctorForm, LoginForm, EditMyUserForm, EditUserForm, EditMyDoctorForm
from user.models import MyUser, Doctor


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
        redirect("/")


@login_required()
def edit_profile(request):
    user = request.user
    myuser = MyUser.objects.get(user=user)
    form_user = EditUserForm(request.POST or None, initial={'first_name': myuser.user.first_name,
                                                            'last_name': myuser.user.last_name,
                                                            'email': myuser.user.email})
    form_myuser = EditMyUserForm(request.POST or None, initial={'phone_number': myuser.phone_number,
                                                                'national_code': myuser.national_code})
    if not myuser.is_doctor:
        if request.method == 'POST':
            # form = EditProfileForm(request.POST)
            if form_user.is_valid() * form_myuser.is_valid():
                user.first_name = form_user.cleaned_data['first_name']
                user.last_name = form_user.cleaned_data['last_name']
                user.email = form_user.cleaned_data['email']
                myuser.phone_number = form_myuser.cleaned_data['phone_number']
                myuser.national_code = form_myuser.cleaned_data['national_code']
                user.save()
                myuser.user = user
                myuser.save()
            return HttpResponseRedirect('/user/profile')
        return render(request, 'user/edit_profile_user.html', {"form_user": form_user, "form_myuser": form_myuser, "myuser": myuser})
    else:
        doctor = Doctor.objects.get(user=myuser)
        form_doctor = EditMyDoctorForm(request.POST or None, initial={'university': doctor.university,
                                                                      'year_diploma': doctor.year_diploma,
                                                                      'diploma': doctor.diploma,
                                                                      'office_address': doctor.office_address,
                                                                      'office_phone_number': doctor.office_phone_number})
        if request.method == 'POST':
            if form_user.is_valid() * form_myuser.is_valid():
                user.first_name = form_user.cleaned_data['first_name']
                user.last_name = form_user.cleaned_data['last_name']
                user.email = form_user.cleaned_data['email']
                myuser.phone_number = form_myuser.cleaned_data['phone_number']
                myuser.national_code = form_myuser.cleaned_data['national_code']
                user.save()
                myuser.user = user
                myuser.save()
            if form_doctor.is_valid():
                doctor.university = form_doctor.cleaned_data['university']
                doctor.year_diploma = form_doctor.cleaned_data['year_diploma']
                doctor.diploma = form_doctor.cleaned_data['diploma']
                doctor.office_address = form_doctor.cleaned_data['office_address']
                doctor.office_phone_number = form_doctor.cleaned_data['office_phone_number']
                doctor.user = myuser
                doctor.save()
            return HttpResponseRedirect('/user/profile')
        return render(request, 'user/edit_profile_doctor.html',
                      {"form_user": form_user, "form_myuser": form_myuser, "form_doctor": form_doctor,
                       "myuser": myuser, "doctor": doctor})


def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        upf = MyUserForm(request.POST, prefix='userprofile')
        df = DoctorForm(request.POST
                        # , request.POST, request.POST, request.POST, request.POST, request.POST,
                        # request.FILES
                        , prefix='doctorprofile'
                        )
        if uf.is_valid() * upf.is_valid():
            user = User.objects.create_user(username=uf.cleaned_data['username'], password=uf.cleaned_data['password'],
                                            first_name=uf.cleaned_data['first_name'],
                                            last_name=uf.cleaned_data['last_name'],
                                            email=uf.cleaned_data['email'])
            user.is_active = True
            user.save()
            userprofile = MyUser(user=user, phone_number=upf.cleaned_data['phone_number'],
                                 national_code=upf.cleaned_data['national_code']
                                 # address=upf.cleaned_data['address']
                                 )
            userprofile.save()
            # print("is df valid:", df.is_valid(), "\n")
            if df.is_valid():
                # print("yes df is valid")
                doctorprofile = Doctor(user=userprofile, university=df.cleaned_data['university'],
                                       year_diploma=df.cleaned_data['year_diploma'],
                                       diploma=df.cleaned_data['diploma'],
                                       office_address=df.cleaned_data['office_address'],
                                       office_phone_number=df.cleaned_data['office_phone_number']
                                       # contract=df.cleaned_data["contract"]
                                       )
                # print(doctorprofile.year_diploma)
                userprofile.is_doctor = True
                userprofile.save()
                # print(userprofile.is_doctor)
                doctorprofile.save()
            return render(request, 'index.html')
    else:
        uf = UserForm(prefix='user')
        upf = MyUserForm(prefix='userprofile')
        df = DoctorForm(prefix='doctorprofile')
    return render(request, 'user/register_user.html', {'userform': uf, 'userprofileform': upf, 'doctorprofile': df})


def login(request):
    message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                findeduser = User.objects.get(pk=user.id)
                my_user = MyUser.objects.get(user=findeduser)

                if findeduser.is_active:
                    if Doctor.objects.filter(user=my_user).count() > 0:
                        doc = Doctor.objects.get(user=my_user)
                        django_login(request, user)
                    else:
                        django_login(request, user)
                    return redirect('/user/')
                else:
                    form = LoginForm()
                    # raise forms.ValidationError('.حساب کاربری شما غیرفعال است.')
                    message = ".حساب کاربری شما غیرفعال است."
            else:
                form = LoginForm()
                # print("pass or username wrong")
                # raise forms.ValidationError('نام کاربری یا گذرواژه شما اشتباه است..')
                message = "نام کاربری یا گذرواژه شما اشتباه است."
    else:
        form = LoginForm()
    return render(request, "user/login_user.html", {'form': form, 'message': message})


def logout(request):
    django_logout(request)
    return redirect('/')
