from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import login, logout, get_user
from django.contrib.auth import update_session_auth_hash
from . import forms


def user_view(request):
    form = UserChangeForm()
    args = {'form': form}
    return render(request, 'Accounts/f.html', args)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    elif request.method == 'GET':
        form = forms.SignupForm()
    else:
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            login(request, user=form.save())
            return redirect('main')
    args = {'form': form}
    return render(request, 'Accounts/signup.html', args)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    elif request.method == 'GET':
        form = forms.LoginForm(request)
    else:
        form = forms.LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, user=form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('main')
    args = {'form': form}
    return render(request, 'Accounts/login.html', args)


def logout_view(request):
    if request.user.is_authenticated:
        is_auth = True
        logout(request)
    is_auth = False
    args = {'is_auth': is_auth, 'username': get_user(request)}
    return render(request, 'Accounts/logout.html', args)


def change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if_code = 1
            form = forms.ChangePassForm(user=request.user)
            args = {'form': form, 'if_code': if_code, 'username': get_user(request)}
            return render(request, 'Accounts/change_pass.html', args)
        else:
            form = forms.ChangePassForm(request.POST, user=request.user)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                logout(request)
                if_code = 2
                args = {'if_code': if_code}
                return render(request, 'Accounts/change_pass.html', args)
            if_code = 1
    else:
        if_code = 3
        args = {'if_code': if_code}
        return render(request, 'Accounts/change_pass.html', args)
    args = {'if_code': if_code, 'form': form, 'username': get_user(request)}
    return render(request, 'Accounts/change_pass.html', args)

