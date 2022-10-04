from django.shortcuts import render
from django.contrib.auth import get_user
from django.contrib.admin.views.decorators import staff_member_required

from Programs import models

from AdminPanel import forms


@staff_member_required
def Admin(request):
    return render(request, 'AdminPanel/admin_main.html', {'username': get_user(request)})


@staff_member_required
def AdminProgram(request):
    programs = models.Program.objects.all().order_by('date_created')
    temp_var = 0
    program_id = request.GET.get('del_id')
    if program_id is not None:
        temp_var = 1
        try:
            if programs.get(id=program_id) is not None:
                temp_var = 2
                program_to_del = programs.get(id=program_id)
                program_to_del.delete()
        except:
            pass
    if programs.count() == 0:
        temp_var = 6
    args = {'programs': programs, 'username': get_user(request), 'temp_var': temp_var}
    return render(request, 'AdminPanel/admin_program.html', args)


@staff_member_required
def AdminProgramAdd(request):
    if request.method == 'GET':
        form = forms.AdminProgramForm()
        args = {'username': get_user(request), 'form': form}
        return render(request, 'AdminPanel/admin_program_add.html', args)
    if request.method == 'POST':
        form = forms.AdminProgramForm(request.POST, request.FILES)
        temp_var = 5
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.last_modified_by = request.user
            obj.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'form': form}
        return render(request, 'AdminPanel/admin_program_add.html', args)


@staff_member_required
def AdminProgramView(request, num):
    try:
        program = models.Program.objects.get(id=num)
        is_exist = True
        args = {'username': get_user(request), 'program': program, 'is_exist': is_exist}
        return render(request, 'AdminPanel/admin_program_view.html', args)
    except:
        is_exist = False
        args = {'is_exist': is_exist}
        return render(request, 'AdminPanel/admin_program_view.html', args)


@staff_member_required
def AdminProgramEdit(request, num):
    if request.method == 'GET':
        try:
            program = models.Program.objects.get(id=num)
            if program.is_active:
                program.is_active = 'checked'
            elif not program.is_active:
                program.is_active = 'unchecked'
            form = forms.AdminProgramForm()
            temp_var = 0
            args = {'username': get_user(request), 'program': program,
                    'temp_var': temp_var, 'form': form,
                    }
            return render(request, 'AdminPanel/admin_program_edit.html', args)
        except:
            temp_var = 4
            args = {'temp_var': temp_var}
            return render(request, 'AdminPanel/admin_program_edit.html', args)

    if request.method == 'POST':
        program = models.Program.objects.get(id=request.POST.get('id'))
        form = forms.AdminProgramForm(request.POST, request.FILES, instance=program)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        if program.is_active:
            program.is_active = 'checked'
        elif not program.is_active:
            program.is_active = 'unchecked'
        args = {'temp_var': temp_var, 'username': get_user(request),
                'program': program, 'form': form,
                }
        return render(request, 'AdminPanel/admin_program_edit.html', args)

