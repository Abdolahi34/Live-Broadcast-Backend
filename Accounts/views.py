from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import login, logout, get_user, decorators
from django.contrib.auth import update_session_auth_hash
from . import forms


@decorators.login_required(login_url='Accounts:login')
def profile_view(request):
    def profile_attrs():
        form.fields['username'].widget.attrs['class'] = 'form-control'
        form.fields['username'].widget.attrs['placeholder'] = 'Username'
        form.fields['first_name'].widget.attrs['class'] = 'form-control'
        form.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        form.fields['last_name'].widget.attrs['class'] = 'form-control'
        form.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        form.fields['email'].widget.attrs['class'] = 'form-control'
        form.fields['email'].widget.attrs['placeholder'] = 'Email Address'
    if request.method == 'GET':
        form = UserChangeForm(instance=request.user)
        if_valid = False
        profile_attrs()
        args = {'form': form, 'username': get_user(request), 'if_valid': if_valid}
        return render(request, 'Accounts/profile.html', args)
    else:
        form = UserChangeForm(request.POST, instance=request.user)
        if_valid = False
        if form.is_valid():
            form.save()
            if_valid = True
        profile_attrs()
        args = {'form': form, 'if_valid': if_valid, 'username': get_user(request)}
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
            if 'next' in request.GET:
                if_code = 2
                args = {'if_code': if_code, 'next_post': request.GET.get('next')}
            else:
                if_code = 3
                args = {'if_code': if_code}
            login(request, user=form.get_user())
            return render(request, 'Accounts/login.html', args)
    args = {'form': form, 'request': request}
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


@decorators.login_required(login_url='Accounts:login')
def profile_view2(request):
    return redirect('Accounts:profile')


def signup_view2(request):
    return redirect('Accounts:signup')


def login_view2(request):
    return redirect('Accounts:login')


def logout_view2(request):
    return redirect('Accounts:logout')


def change_pass2(request):
    return redirect('Accounts:change_pass')

