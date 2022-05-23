from django import forms
from account.models import User

class LoginForm(forms.Form):
    login = forms.CharField(max_length=32, label='Login')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email_address']
