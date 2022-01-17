from django.contrib.auth import password_validation
from django import forms
from django.forms import widgets
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label='Username :',
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
    }))
    password = forms.CharField(
        label='Password :',
        widget=widgets.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'Password',
    }))


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'Password',
        }),
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'Password Confirmation',
        }),
    )


class ChangePassForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'autofocus': True,
            'class': 'form-control password-field',
            'placeholder': 'Old Password',
        }),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control password-field',
            'placeholder': 'New password',
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control password-field',
            'placeholder': 'New password confirmation'
        }),
    )

