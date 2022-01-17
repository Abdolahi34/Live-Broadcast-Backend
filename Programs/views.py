from django.shortcuts import render, redirect
from . import models, forms
from BroadcastSite.views import etc
from django.contrib.auth.decorators import permission_required,login_required
from django.contrib.auth import get_user


def program(request):
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


@login_required(login_url='Accounts:login')
@permission_required('Programs.add_program', login_url='access_denied')
def add_program(request):
    if_code = False
    if request.method == 'GET':
        form = forms.AddProgramForm()
    else:
        form = forms.AddProgramForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if_code = True
    args = {'form': form, 'if_code': if_code, 'username': get_user(request)}
    return render(request, 'Programs/program_add.html', args)


def add_program2(request):
    return redirect('Programs:add_program')


# def view_program(request,slug):
#     all_programs = models.Program.objects.all().get(slug=slug)
#     return render(request, 'Programs/program_view.html', {'all_programs': all_programs})
    # return render(request, 'Programs/program_view.html')

