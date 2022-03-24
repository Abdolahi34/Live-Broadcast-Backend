from django.shortcuts import render, HttpResponse
from django.views import View
from django.core.mail import send_mail
from django.conf import settings


def status_code_403_forbidden(request, exception=None):
    return render(request, 'LesanLive/403.html', status=403)


def status_code_404_not_found(request, exception=None):
    return render(request, 'LesanLive/404.html', status=404)


def status_code_500_internal_server_error(request, exception=None):
    return render(request, 'LesanLive/500.html', status=500)


class Home(View):
    def get(self, request):
        return HttpResponse('پخش زنده - لسان صدق')


class ContactUs(View):
    def get(self, request):
        return render(request, 'LesanLive/contact_us.html')

    def post(self, request):
        subject = 'فرم ContactUs'
        message = f"موضوع : {request.POST.get('subject')}\n\nاز طرف : \nنام : {request.POST.get('name')}\nایمیل : {request.POST.get('email')}\n\nپیغام : {request.POST.get('message')}"
        recipient_list = ['admin@radio.rahh.ir']  # TODO
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return render(request, 'LesanLive/contact_us_done.html')
