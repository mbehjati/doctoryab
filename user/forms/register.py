# -*- coding: UTF-8 -*-
from django import forms
from django.contrib.auth.models import User

from user.models import MyUser, Doctor


class UserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.widgets.PasswordInput, label='تکرار گذرواژه')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        _password = cleaned_data.get('password')
        _password2 = cleaned_data.get('password2')

        if _password2 and _password and _password2 != _password:
            raise forms.ValidationError('تکرار گذرواژه اشتباه است.')
        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput,
            'password2': forms.PasswordInput,
            'email': forms.EmailInput
        }
        labels = {
            'username': 'نام‌کاربری',
            'password': 'گذواژه',
            'password2': 'تکرار گذرواژه',
            'first_name': 'نام',
            'last_name': 'نام خانواگی',
            'email': 'ایمیل'
        }


class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        exclude = ['user', 'is_doctor']
        labels = {
            'phone_number': "شماره تلفن",
            'national_code': "کد ملی"
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user']

        labels = {
            'diploma': 'مدرک',
            'year_diploma': 'سال اخذ مدرک',
            'office_address': 'آدرس مطب',
            'office_phone_number': 'شماره تلفن مطب',
            'university': 'دانشگاه',
            'expertise': 'تخصص',
            'insurance': 'بیمه',
        }