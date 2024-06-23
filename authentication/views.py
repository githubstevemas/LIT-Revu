from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from authentication.models import User

from . import forms


def logout_user(request):
    # Log out logged user and redirect tou login page
    logout(request)
    return redirect('login')


def login_page(request):
    # Initialize login form
    form = forms.LoginForm()
    message = ''
    # If request.method is POST user, use POST data for login form
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        # If valid, authenticate and login
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
        request, 'authentication/login.html', context={
            'form': form,
            'message': message
        })


def signup_page(request):
    # Initialize signup form
    form = forms.SignupForm()
    # If request.method is POST user, use POST data for signup form
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        # If valid, save data and log current user
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(
        request, 'authentication/signup.html',
        context={'form': form}
    )


@login_required()
def user_page(request, user_id):
    # Get user object with user_id
    user = get_object_or_404(User, id=user_id)

    return render(
        request, 'authentication/user.html',
        {'user': user}
    )
