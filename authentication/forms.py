from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='Password')
