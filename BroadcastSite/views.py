from django.shortcuts import redirect, render, HttpResponse
from django.http import Http404


def main(request):
    return redirect('Programs:program')


def login_redirect(request):
    return redirect('Accounts:login')


def signup_redirect(request):
    return redirect('Accounts:signup')


def logout_redirect(request):
    return redirect('Accounts:logout')


def change_pass_redirect(request):
    return redirect('Accounts:change_pass')


def profile_view_redirect(request):
    return redirect('Accounts:profile')


def program_redirect(request):
    return redirect('Programs:program')


def access_denied(request):
    return render(request, 'BroadcastSite/access_denied.html')


def etc(request, etc):
    raise Http404()

