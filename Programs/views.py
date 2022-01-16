from django.shortcuts import render, HttpResponse
from . import models
from BroadcastSite.views import etc
from django.contrib.auth.decorators import login_required


def programs(request):
    # Angular
    pass


def stream(request, title_slug, stream_slug):
    program_obj = models.Program.objects.all()
    title_slugs = []
    stream_slugs = []
    for program in program_obj:
        title_slugs.append(program.slug)
        stream_slugs.append(program.stream_slug)
    if title_slug in title_slugs and stream_slug in stream_slugs:
        # return HttpResponse('<h1>Stream Page</h1>')
        pass
    else:
        etc()


@login_required(login_url='Accounts:login')
def add_program(request):
    pass

