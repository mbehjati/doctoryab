from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='username')
    password = forms.CharField(widget=forms.widgets.PasswordInput, label="password")

    class Meta:
        fields = ['username', 'password']


'''    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
                # TODO with manager activation
                # or not user.is_active:
            raise forms.ValidationError("Login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
'''
