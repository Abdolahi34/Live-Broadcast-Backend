from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator


from Programs import models

from Admin import forms

# @method_decorator(login_required(login_url='Accounts:login'), name='dispatch')
# @method_decorator(permission_required('Programs.add_program', raise_exception=True), name='dispatch')
class Admin(View):
    def get(self, request):
        args = {'username': get_user(request)}
        return render(request, 'Admin/admin_main.html', args)


class AdminProgram(View):
    def get(self, request):
        programs = models.Program.objects.all().order_by('date_created')
        temp_var = 0
        program_id = request.GET.get('del_id')
        if program_id != None:
            temp_var = 1
            try:
                if programs.get(id=program_id) != None:
                    temp_var = 2
                    program_to_del = programs.get(id=program_id)
                    program_to_del.delete()
            except:
                pass
        if programs.count() == 0:
            temp_var = 6
        args = {'programs': programs, 'username': get_user(request), 'temp_var': temp_var}
        return render(request, 'Admin/admin_program.html', args)


class AdminProgramView(View):
    def get(self, request, num):
        try:
            program = models.Program.objects.get(id=num)
            is_exist = True
            args = {'username': get_user(request), 'program': program, 'is_exist': is_exist}
            return render(request, 'Admin/admin_program_view.html', args)
        except:
            is_exist = False
            args = {'is_exist': is_exist}
            return render(request, 'Admin/admin_program_view.html', args)


# TODO
class AdminProgramEdit(View):
    def get(self, request, num):
        try:
            program = models.Program.objects.get(id=num)
            form = forms.AdminProgramEditForm()
            temp_var = 0
            args = {'username': get_user(request), 'program': program,
                    'temp_var': temp_var, 'form': form,
                    }
            return render(request, 'Admin/admin_program_edit.html', args)
        except:
            temp_var = 4
            args = {'temp_var': temp_var, 'username': get_user(request)}
            return render(request, 'Admin/admin_program_edit.html', args)

    def post(self, request, *args, **kwargs):
        form = forms.AdminProgramEditForm(request.POST, request.FILES)
        program = models.Program.objects.get(id=request.POST.get('id'))
        if request.POST.get('logo') == '':
            form.logo = program.logo.path
        if form.is_valid():
            if program.slug != form.slug:
                program.slug = form.slug
            if program.num_order != form.num_order:
                program.num_order = form.num_order
            program.title = form.title
            program.datetype = form.datetype
            program.start_time = form.start_time
            program.end_time = form.end_time
            program.logo_onclick_link = form.logo_onclick_link
            program.logo = form.logo
            program.stream = form.stream
            program.is_active = form.is_active
            program.save()

            temp_var = 3
            args = {'temp_var': temp_var, 'username': get_user(request)}
            return render(request, 'Admin/admin_program.html', args)
        temp_var = 5
        args = {'temp_var': temp_var, 'username': get_user(request),
                'program': program, 'form': form,
                }
        return render(request, 'Admin/admin_program_edit.html', args)


class AdminDateType(View):
    def get(self, request):
        datetypes = models.DateType.objects.all().order_by('id')
        temp_var = 0
        datetype_id = request.GET.get('del_id')
        if datetype_id != None:
            temp_var = 1
            try:
                if datetypes.get(id=datetype_id) != None:
                    temp_var = 2
                    datetype_to_del = datetypes.get(id=datetype_id)
                    datetype_to_del.delete()
            except:
                pass
        if datetypes.count() == 0:
            temp_var = 6
        args = {'datetypes': datetypes, 'username': get_user(request), 'temp_var': temp_var}
        return render(request, 'Admin/admin_datetype.html', args)


class AdminDateTypeView(View):
    def get(self, request, num):
        try:
            datetype = models.DateType.objects.get(id=num)
            is_exist = True
            args = {'username': get_user(request), 'datetype': datetype, 'is_exist': is_exist}
            return render(request, 'Admin/admin_datetype_view.html', args)
        except:
            is_exist = False
            args = {'is_exist': is_exist}
            return render(request, 'Admin/admin_datetype_view.html', args)


class AdminDateTypeEdit(View):
    def get(self, request):
        pass


class AdminStreamType(View):
    def get(self, request):
        programs = models.Program.objects.all().order_by('date_created')
        temp_var = 0
        program_id = request.GET.get('del_id')
        if program_id != None:
            temp_var = 1
            try:
                if programs.get(id=program_id) != None:
                    temp_var = 2
                    program_to_del = programs.get(id=program_id)
                    program_to_del.delete()
            except:
                pass
        if programs.count() == 0:
            temp_var = 6
        args = {'programs': programs, 'username': get_user(request), 'temp_var': temp_var}
        return render(request, 'Admin/admin_program.html', args)


class AdminStreamTypeView(View):
    def get(self, request, num):
        try:
            program = models.Program.objects.get(id=num)
            is_exist = True
            args = {'username': get_user(request), 'program': program, 'is_exist': is_exist}
            return render(request, 'Admin/admin_program_view.html', args)
        except:
            is_exist = False
            args = {'is_exist': is_exist}
            return render(request, 'Admin/admin_program_view.html', args)


class AdminStreamTypeEdit(View):
    def get(self, request):
        pass


class AdminVideoContent(View):
    def get(self, request):
        programs = models.Program.objects.all().order_by('date_created')
        temp_var = 0
        program_id = request.GET.get('del_id')
        if program_id != None:
            temp_var = 1
            try:
                if programs.get(id=program_id) != None:
                    temp_var = 2
                    program_to_del = programs.get(id=program_id)
                    program_to_del.delete()
            except:
                pass
        if programs.count() == 0:
            temp_var = 6
        args = {'programs': programs, 'username': get_user(request), 'temp_var': temp_var}
        return render(request, 'Admin/admin_program.html', args)


class AdminVideoContentView(View):
    def get(self, request, num):
        try:
            program = models.Program.objects.get(id=num)
            is_exist = True
            args = {'username': get_user(request), 'program': program, 'is_exist': is_exist}
            return render(request, 'Admin/admin_program_view.html', args)
        except:
            is_exist = False
            args = {'is_exist': is_exist}
            return render(request, 'Admin/admin_program_view.html', args)


class AdminVideoContentEdit(View):
    def get(self, request):
        pass


class AdminVideoStat(View):
    def get(self, request):
        programs = models.Program.objects.all().order_by('date_created')
        temp_var = 0
        program_id = request.GET.get('del_id')
        if program_id != None:
            temp_var = 1
            try:
                if programs.get(id=program_id) != None:
                    temp_var = 2
                    program_to_del = programs.get(id=program_id)
                    program_to_del.delete()
            except:
                pass
        if programs.count() == 0:
            temp_var = 6
        args = {'programs': programs, 'username': get_user(request), 'temp_var': temp_var}
        return render(request, 'Admin/admin_program.html', args)


class AdminVideoStatView(View):
    def get(self, request, num):
        try:
            program = models.Program.objects.get(id=num)
            is_exist = True
            args = {'username': get_user(request), 'program': program, 'is_exist': is_exist}
            return render(request, 'Admin/admin_program_view.html', args)
        except:
            is_exist = False
            args = {'is_exist': is_exist}
            return render(request, 'Admin/admin_program_view.html', args)


class AdminVideoStatEdit(View):
    def get(self, request):
        pass


class AdminVoiceContent(View):
    def get(self, request):
        programs = models.Program.objects.all().order_by('date_created')
        temp_var = 0
        program_id = request.GET.get('del_id')
        if program_id != None:
            temp_var = 1
            try:
                if programs.get(id=program_id) != None:
                    temp_var = 2
                    program_to_del = programs.get(id=program_id)
                    program_to_del.delete()
            except:
                pass
        if programs.count() == 0:
            temp_var = 6
        args = {'programs': programs, 'username': get_user(request), 'temp_var': temp_var}
        return render(request, 'Admin/admin_program.html', args)


class AdminVoiceContentView(View):
    def get(self, request, num):
        try:
            program = models.Program.objects.get(id=num)
            is_exist = True
            args = {'username': get_user(request), 'program': program, 'is_exist': is_exist}
            return render(request, 'Admin/admin_program_view.html', args)
        except:
            is_exist = False
            args = {'is_exist': is_exist}
            return render(request, 'Admin/admin_program_view.html', args)


class AdminVoiceContentEdit(View):
    def get(self, request):
        pass


class AdminVoiceStat(View):
    def get(self, request):
        programs = models.Program.objects.all().order_by('date_created')
        temp_var = 0
        program_id = request.GET.get('del_id')
        if program_id != None:
            temp_var = 1
            try:
                if programs.get(id=program_id) != None:
                    temp_var = 2
                    program_to_del = programs.get(id=program_id)
                    program_to_del.delete()
            except:
                pass
        if programs.count() == 0:
            temp_var = 6
        args = {'programs': programs, 'username': get_user(request), 'temp_var': temp_var}
        return render(request, 'Admin/admin_program.html', args)


class AdminVoiceStatView(View):
    def get(self, request, num):
        try:
            program = models.Program.objects.get(id=num)
            is_exist = True
            args = {'username': get_user(request), 'program': program, 'is_exist': is_exist}
            return render(request, 'Admin/admin_program_view.html', args)
        except:
            is_exist = False
            args = {'is_exist': is_exist}
            return render(request, 'Admin/admin_program_view.html', args)


class AdminVoiceStatEdit(View):
    def get(self, request):
        pass
