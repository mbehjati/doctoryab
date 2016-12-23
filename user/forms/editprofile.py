from django import forms
from django.contrib.auth.models import User
from user.models import MyUser, Doctor


class EditUserForm(forms.ModelForm):
    # first_name = forms.CharField(label='First Name')
    # last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EditMyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        exclude = ['user', 'is_doctor']


class EditMyDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user']
# , 'contract']
