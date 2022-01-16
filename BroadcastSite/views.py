from django.shortcuts import redirect, render, HttpResponse
from django.http import Http404


def etc(request, etc):
    raise Http404()


def main(request):
    # HttpResponse('<h1>Home Page</h1>')
    return redirect('Programs:programs')


def login_view(request):
    return redirect('Accounts:login')


def signup_view(request):
    return redirect('Accounts:signup')


def logout_view(request):
    return redirect('Accounts:logout')


def change_pass(request):
    return redirect('Accounts:change_pass')

