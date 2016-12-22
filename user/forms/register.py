from django import forms
from user.models import MyUser
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.widgets.PasswordInput, label="Password(again)")

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
        }


class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        exclude = ['user']
