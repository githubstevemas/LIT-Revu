from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from authentication.models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, label='Username')
    password = forms.CharField(max_length=15, widget=forms.PasswordInput, label='Password')


class AccountForm(forms.ModelForm):
    profile_photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'profile-photo-input'})
    )

    class Meta:
        model = User
        fields = ['profile_photo']
