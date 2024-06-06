from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.conf import settings

from . import forms


class LoginPage(View):

    from_class = forms.LoginForm
    template_name = 'authentication/login.html'

    def get(self, request):

        form = self.from_class
        message = ''
        return render(
            request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):

        form = self.from_class(request.POST)
        message = ''

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = "Wrong id"

        return render(
            request, self.template_name, context={'form': form, 'message': message})


def logout_user(request):
    logout(request)
    return redirect('login')


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = "Wrong id"

    return render(
        request, 'authentication/login.html', context={'form': form, 'message': message}
    )


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'authentication/signup.html', context={'form': form})
