# -*- coding: UTF-8 -*-

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='نام کاربری')
    password = forms.CharField(widget=forms.widgets.PasswordInput, label="گذرواژه")

    class Meta:
        fields = ['username', 'password']
