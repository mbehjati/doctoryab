# -*- coding: UTF-8 -*-
from django import forms
from django.contrib.auth.models import User
from user.models import MyUser, Doctor


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label='نام‌کاربری', required=True)
    password = forms.CharField(widget=forms.widgets.PasswordInput, label=' گذرواژه', required=True)
    password2 = forms.CharField(widget=forms.widgets.PasswordInput, label='تکرار گذرواژه', required=True)
    first_name = forms.CharField(max_length=100, label='نام', required=False)
    last_name = forms.CharField(max_length=100, label='نام خانواگی', required=False)
    email = forms.EmailField(max_length=100, label='ایمیل', required=False)

    def __init__(self, *args, **kwargs):
        self.register_form = kwargs.pop('for_register', False)
        self.edit_form = kwargs.pop('for_edit_profile', False)
        super(UserForm, self).__init__(*args, **kwargs)
        if self.edit_form:
            del self.fields['username']
            del self.fields['password']
            del self.fields['password2']
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        _password = cleaned_data.get('password')
        _password2 = cleaned_data.get('password2')

        if _password2 and _password and _password2 != _password:
            raise forms.ValidationError('تکرار گذرواژه اشتباه است.')
        if User.objects.filter(username=cleaned_data.get('username')).count():
            raise forms.ValidationError('نام کاربری قبلاً ثبت شده است.')
        return cleaned_data

    class Meta:
        model = MyUser
        exclude = ['user', 'is_doctor']
        fields = ['username', 'password', 'password2', 'first_name', 'last_name',
                  'email', 'national_code', 'phone_number', 'image']
        widgets = {
            'password': forms.PasswordInput,
            'password2': forms.PasswordInput,
            'email': forms.EmailInput,
            'image': forms.FileInput
        }
        labels = {
            'phone_number': "شماره تلفن",
            'national_code': "کد ملی"
        }

    def save(self, commit=True, *args, **kwargs):
        user = kwargs.get('user')
        # existed_my_user = kwargs.get('my_user')
        my_user = super(UserForm, self).save(commit=False)

        if self.register_form:
            my_user = self.register_my_user(my_user=my_user)
            if commit:
                my_user.save()
            return my_user

        elif self.edit_form:
            self.edit_my_user(user=user)
            if commit:
                self.instance.save()
            return self.instance

    def register_my_user(self, my_user):
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        password=self.cleaned_data['password'],
                                        first_name=self.cleaned_data['first_name'],
                                        last_name=self.cleaned_data['last_name'],
                                        email=self.cleaned_data['email'])
        user.is_active = True
        my_user.user = user
        return my_user

    def edit_my_user(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        self.instance.user = user


class DoctorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.register_form = kwargs.pop('for_register', False)
        self.edit_form = kwargs.pop('for_edit_profile', False)
        super(DoctorForm, self).__init__(*args, **kwargs)
        if self.edit_form:
            del self.fields['contract']

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

    def save(self, commit=True, *args, **kwargs):
        user = kwargs.get('user')
        doctor = super(DoctorForm, self).save(commit=False)

        if self.register_form:
            doctor = self.register_doctor(user=user, doctor=doctor)
            doctor.user = user
            doctor.save()
            for ins in self.cleaned_data['insurance']:
                doctor.insurance.add(ins)

            if commit:
                doctor.save()
            return doctor

        elif self.edit_form:
            self.instance.insurance = self.cleaned_data['insurance']
            self.instance.user = user

            if commit:
                self.instance.save()
            return self.instance
