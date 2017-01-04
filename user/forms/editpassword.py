# -*- coding: UTF-8 -*-
from django import forms
from django.contrib.auth.models import User


class EditPasswordForm(forms.Form):
    pre_pass = forms.CharField(max_length=20, widget=forms.PasswordInput, label='رمز عبور قبلی')
    new_pass = forms.CharField(max_length=20, widget=forms.PasswordInput, label='رمز عبور جدید')
    pass_conf = forms.CharField(max_length=20, widget=forms.PasswordInput, label='تایید رمز عبور جدید')

    def __init__(self, *args, **kwargs):
        main_username = kwargs.pop("username")
        super(EditPasswordForm, self).__init__(*args, **kwargs)
        self.user = User.objects.get(username=main_username)

    def clean(self):
        cleaned_data = super(EditPasswordForm, self).clean()

        pre_pass = cleaned_data['pre_pass']
        new_pass = cleaned_data['new_pass']
        new_pass_conf = cleaned_data['pass_conf']
        if not self.user.check_password(pre_pass):
            raise forms.ValidationError("کلمه عبور قبلی اشتباه است.")
        else:
            if new_pass != new_pass_conf:
                raise forms.ValidationError("تکرار کلمه عبور نادرست است.")
        return cleaned_data
