from django.shortcuts import render, HttpResponse
from . import models, forms
from BroadcastSite.views import etc
from django.contrib.auth.decorators import permission_required,login_required


def programs(request):
    # Angular
    pass

# TODO
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


# TODO
@login_required(login_url='Accounts:login')
@permission_required(['Programs_program.can_add_program'])
def add_program(request):
    if request.method == 'GET':
        form = forms.AddProgramForm()
    else:
        form = forms.AddProgramForm(request.POST, request.FILES)
        if form.is_valid():
            pass
    args = {'form': form}
    return render(request, 'BroadcastSite/access_denied.html', args)

