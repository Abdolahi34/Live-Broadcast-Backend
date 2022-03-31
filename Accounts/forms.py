from django.contrib.auth import password_validation
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from captcha.widgets import ReCaptchaV2Checkbox
from captcha.fields import ReCaptchaField


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label='نام کاربری :',
    )
    password = forms.CharField(
        label='رمز عبور :',
    )
    # re_captcha = ReCaptchaField(
    #     widget=ReCaptchaV2Checkbox,
    # )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")

    password1 = forms.CharField(
        label='پسورد',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'پسورد',
        }),
    )
    password2 = forms.CharField(
        label='تایید پسورد',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'تایید پسورد',
        }),
    )
    re_captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
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
    re_captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
    )
