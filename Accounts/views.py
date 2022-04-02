from django.shortcuts import render

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import login, logout, get_user, decorators, update_session_auth_hash, models

from django.views.generic import View

from django.utils.decorators import method_decorator

from Accounts import forms



@method_decorator(decorators.login_required(login_url='Accounts:login'), name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = forms.ProfileForm(instance=request.user)
        if_valid = False
        args = {'form': form, 'username': get_user(request), 'if_valid': if_valid}
        return render(request, 'Accounts/profile.html', args)

    def post(self, request):
        form = forms.ProfileForm(request.POST, instance=request.user)
        if_valid = False
        if form.is_valid():
            form.save()
            if_valid = True
        args = {'form': form, 'if_valid': if_valid, 'username': get_user(request)}
        return render(request, 'Accounts/profile.html', args)


class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if_code = 1
            args = {'if_code': if_code}
            return render(request, 'Accounts/signup.html', args)

        form = forms.SignupForm()
        args = {'form': form}
        return render(request, 'Accounts/signup.html', args)

    def post(self, request):
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            if_code = 2
            args = {'if_code': if_code}
            return render(request, 'Accounts/signup.html', args)
        args = {'form': form}
        return render(request, 'Accounts/signup.html', args)


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if_code = 1
            args = {'if_code': if_code}
            return render(request, 'Accounts/login.html', args)
        form = forms.LoginForm(request)
        args = {'form': form, 'request': request}
        return render(request, 'Accounts/login.html', args)

    def post(self, request):
        form = forms.LoginForm(request, data=request.POST)
        args = {'form': form, 'request': request}
        if form.is_valid():
            if 'next' in request.GET:
                if_code = 2
                args = {'if_code': if_code, 'next_post': request.GET.get('next')}
            else:
                if_code = 3
                args = {'if_code': if_code}
            login(request, user=form.get_user())
        return render(request, 'Accounts/login.html', args)


class LogoutView(View):
    def get(self, request):
        is_auth = False
        args = {'is_auth': is_auth}
        if request.user.is_authenticated:
            is_auth = True
            user_username = get_user(request)
            args = {'is_auth': is_auth, 'username': user_username}
            logout(request)
        return render(request, 'Accounts/logout.html', args)


class ChangePass(View):
    def get(self, request):
        if not request.user.is_authenticated:
            if_code = 1
            args = {'if_code': if_code}
            return render(request, 'Accounts/change_pass.html', args)
        form = forms.ChangePassForm(request.user)
        args = {'form': form, 'username': get_user(request)}
        return render(request, 'Accounts/change_pass.html', args)

    def post(self, request):
        form = forms.ChangePassForm(request.user, request.POST)
        args = {'form': form, 'username': request.user}
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            logout(request)
            if_code = 2
            args = {'if_code': if_code}
        return render(request, 'Accounts/change_pass.html', args)
