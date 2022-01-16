from django.shortcuts import render
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import login, logout, get_user, decorators
from django.contrib.auth import update_session_auth_hash
from . import forms


def user_view(request):
    form = UserChangeForm()
    args = {'form': form, 'a': get_user(request)}
    return render(request, 'Accounts/profile.html', args)


def signup_view(request):
    if request.user.is_authenticated:
        if_code = 1
        args = {'if_code': if_code}
        return render(request, 'Accounts/signup.html', args)
    elif request.method == 'GET':
        form = forms.SignupForm()
    else:
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            login(request, user=form.save())
            if 'next' in request.POST:
                if_code = 2
                args = {'if_code': if_code, 'next_post': request.POST.get('next')}
                return render(request, 'Accounts/signup.html', args)
            else:
                if_code = 3
                args = {'if_code': if_code}
                return render(request, 'Accounts/signup.html', args)
    args = {'form': form}
    return render(request, 'Accounts/signup.html', args)


def login_view(request):
    if request.user.is_authenticated:
        if_code = 1
        args = {'if_code': if_code}
        return render(request, 'Accounts/login.html', args)
    elif request.method == 'GET':
        form = forms.LoginForm(request)
    else:
        form = forms.LoginForm(request, data=request.POST)
        if form.is_valid():
            if 'next' in request.POST:
                if_code = 2
                args = {'if_code': if_code, 'next_post': request.POST.get('next')}
            else:
                if_code = 3
                args = {'if_code': if_code}
            login(request, user=form.get_user())
            return render(request, 'Accounts/login.html', args)
    args = {'form': form}
    return render(request, 'Accounts/login.html', args)


def logout_view(request):
    is_auth = False
    args = {'is_auth': is_auth}
    if request.user.is_authenticated:
        is_auth = True
        user_username = get_user(request)
        args = {'is_auth': is_auth, 'username': user_username}
        logout(request)
    return render(request, 'Accounts/logout.html', args)


def change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            form = forms.ChangePassForm(request.user)
            args = {'form': form, 'username': get_user(request)}
            return render(request, 'Accounts/change_pass.html', args)
        else:
            form = forms.ChangePassForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                logout(request)
                if_code = 1
                args = {'if_code': if_code}
                return render(request, 'Accounts/change_pass.html', args)
            args = {'form': form, 'username': request.user}
            return render(request, 'Accounts/change_pass.html', args)
    else:
        if_code = 2
        args = {'if_code': if_code}
        return render(request, 'Accounts/change_pass.html', args)

