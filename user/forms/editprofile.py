# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.models import User

from user.models import MyUser, Doctor


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "email": "ایمیل"
        }


class EditMyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        exclude = ['user', 'is_doctor']
        labels = {
            'phone_number': "شماره تلفن",
            'national_code': "کد ملی"
        }


class EditMyDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user', 'contract']

        labels = {
            'diploma': 'مدرک',
            'year_diploma': 'سال اخذ مدرک',
            'office_address': 'آدرس مطب',
            'office_phone_number': 'شماره تلفن مطب',
            'university': 'دانشگاه',
            'expertise': 'تخصص',
            'insurance': 'بیمه'
        }
