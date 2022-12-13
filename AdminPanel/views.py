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
    programs = models.Program.objects.all().order_by('-status', 'timestamp_earliest')
    program_id = request.GET.get('delete_id')
    is_exist = True
    is_deleted = False
    if program_id is not None:
        try:
            if programs.get(pk=program_id) is not None:
                program_to_del = programs.get(pk=program_id)
                program_to_del.delete()
                is_deleted = True
        except:
            is_exist = False
    program_null = False
    if programs.count() == 0:
        program_null = True
    args = {'programs': programs, 'username': get_user(request), 'is_exist': is_exist, 'is_deleted': is_deleted,
            'program_null': program_null}
    return render(request, 'AdminPanel/admin_program.html', args)


@staff_member_required
def AdminProgramAdd(request):
    if request.method == 'GET':
        form = forms.AdminAddProgramForm()
        specified_date = None
        specified_start_time = None
        specified_end_time = None
        is_add = True
        args = {'username': get_user(request), 'form': form, 'is_add': is_add, 'specified_date': specified_date,
                'specified_start_time': specified_start_time, 'specified_end_time': specified_end_time}
        return render(request, 'AdminPanel/admin_program_add_edit.html', args)
    elif request.method == 'POST':
        is_valid = False
        specified_date = None
        specified_start_time = None
        specified_end_time = None
        change_data = request.POST.copy()
        if change_data['datetime_type'] != 'weekly':
            # Set occasional
            list_specified_date = change_data['list_specified_date']
            list_specified_date_splitted = list_specified_date.split(",")
            list_specified_date_splitted = list(dict.fromkeys(list_specified_date_splitted))
            list_specified_date_removed = change_data['list_specified_date_removed']
            list_specified_date_removed_splitted = list_specified_date_removed.split(",")
            list_specified_date_removed_splitted = list(dict.fromkeys(list_specified_date_removed_splitted))
            list_specified_date_splitted = [item for item in list_specified_date_splitted if
                                            item not in list_specified_date_removed_splitted]
            change_data['specified_date'] = []
            for i in list_specified_date_splitted:
                try:
                    if change_data[i] != '' and change_data[i] is not None:
                        change_data['specified_date'].append(change_data[i])
                except:
                    pass

            list_specified_start_time = change_data['list_specified_start_time']
            list_specified_start_time_splitted = list_specified_start_time.split(",")
            list_specified_start_time_splitted = list(dict.fromkeys(list_specified_start_time_splitted))
            list_specified_start_time_removed = change_data['list_specified_start_time_removed']
            list_specified_start_time_removed_splitted = list_specified_start_time_removed.split(",")
            list_specified_start_time_removed_splitted = list(dict.fromkeys(list_specified_start_time_removed_splitted))
            list_specified_start_time_splitted = [item for item in list_specified_start_time_splitted if
                                                  item not in list_specified_start_time_removed_splitted]
            change_data['specified_start_time'] = []
            for i in list_specified_start_time_splitted:
                try:
                    if change_data[i] != '' and change_data[i] is not None:
                        change_data['specified_start_time'].append(change_data[i])
                except:
                    pass

            list_specified_end_time = change_data['list_specified_end_time']
            list_specified_end_time_splitted = list_specified_end_time.split(",")
            list_specified_end_time_splitted = list(dict.fromkeys(list_specified_end_time_splitted))
            list_specified_end_time_removed = change_data['list_specified_end_time_removed']
            list_specified_end_time_removed_splitted = list_specified_end_time_removed.split(",")
            list_specified_end_time_removed_splitted = list(dict.fromkeys(list_specified_end_time_removed_splitted))
            list_specified_end_time_splitted = [item for item in list_specified_end_time_splitted if
                                                item not in list_specified_end_time_removed_splitted]
            change_data['specified_end_time'] = []
            for i in list_specified_end_time_splitted:
                try:
                    if change_data[i] != '' and change_data[i] is not None:
                        change_data['specified_end_time'].append(change_data[i])
                except:
                    pass

            if change_data['datetime_type'] == 'occasional':
                # None weekly
                change_data['start_date'] = None
                change_data['end_date'] = None
                change_data['day_0'] = None
                change_data['start_time_day_0'] = None
                change_data['end_time_day_0'] = None
                change_data['day_1'] = None
                change_data['start_time_day_1'] = None
                change_data['end_time_day_1'] = None
                change_data['day_2'] = None
                change_data['start_time_day_2'] = None
                change_data['end_time_day_2'] = None
                change_data['day_3'] = None
                change_data['start_time_day_3'] = None
                change_data['end_time_day_3'] = None
                change_data['day_4'] = None
                change_data['start_time_day_4'] = None
                change_data['end_time_day_4'] = None
                change_data['day_5'] = None
                change_data['start_time_day_5'] = None
                change_data['end_time_day_5'] = None
                change_data['day_6'] = None
                change_data['start_time_day_6'] = None
                change_data['end_time_day_6'] = None
        else:
            # None occasional
            change_data['specified_date'] = None
            change_data['specified_start_time'] = None
            change_data['specified_end_time'] = None
        form = forms.AdminAddProgramForm(change_data, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.latest_modifier = request.user
            obj.save()
            is_valid = True
        else:
            specified_date = change_data['specified_date']
            specified_start_time = change_data['specified_start_time']
            specified_end_time = change_data['specified_end_time']
        is_add = True
        args = {'is_valid': is_valid, 'is_add': is_add, 'username': get_user(request), 'form': form,
                'specified_date': specified_date, 'specified_start_time': specified_start_time,
                'specified_end_time': specified_end_time}
        return render(request, 'AdminPanel/admin_program_add_edit.html', args)


@staff_member_required
def AdminProgramView(request, num):
    try:
        program = models.Program.objects.get(pk=num)
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
            program = models.Program.objects.get(pk=num)
            form = forms.AdminAddProgramForm()
            specified_date = program.specified_date
            specified_start_time = program.specified_start_time
            specified_end_time = program.specified_end_time
            is_edit = True
            args = {'username': get_user(request), 'program': program, 'form': form, 'is_edit': is_edit,
                    'specified_date': specified_date, 'specified_start_time': specified_start_time,
                    'specified_end_time': specified_end_time}
            return render(request, 'AdminPanel/admin_program_add_edit.html', args)
        except:
            is_exist = False
            args = {'is_exist': is_exist}
            return render(request, 'AdminPanel/admin_program_add_edit.html', args)

    if request.method == 'POST':
        is_valid = False
        specified_date = None
        specified_start_time = None
        specified_end_time = None
        change_data = request.POST.copy()
        if change_data['datetime_type'] != 'weekly':
            # Set occasional
            list_specified_date = change_data['list_specified_date']
            list_specified_date_splitted = list_specified_date.split(",")
            list_specified_date_splitted = list(dict.fromkeys(list_specified_date_splitted))
            list_specified_date_removed = change_data['list_specified_date_removed']
            list_specified_date_removed_splitted = list_specified_date_removed.split(",")
            list_specified_date_removed_splitted = list(dict.fromkeys(list_specified_date_removed_splitted))
            list_specified_date_splitted = [item for item in list_specified_date_splitted if
                                            item not in list_specified_date_removed_splitted]
            change_data['specified_date'] = []
            for i in list_specified_date_splitted:
                try:
                    if change_data[i] != '' and change_data[i] is not None:
                        change_data['specified_date'].append(change_data[i])
                except:
                    pass

            list_specified_start_time = change_data['list_specified_start_time']
            list_specified_start_time_splitted = list_specified_start_time.split(",")
            list_specified_start_time_splitted = list(dict.fromkeys(list_specified_start_time_splitted))
            list_specified_start_time_removed = change_data['list_specified_start_time_removed']
            list_specified_start_time_removed_splitted = list_specified_start_time_removed.split(",")
            list_specified_start_time_removed_splitted = list(dict.fromkeys(list_specified_start_time_removed_splitted))
            list_specified_start_time_splitted = [item for item in list_specified_start_time_splitted if
                                                  item not in list_specified_start_time_removed_splitted]
            change_data['specified_start_time'] = []
            for i in list_specified_start_time_splitted:
                try:
                    if change_data[i] != '' and change_data[i] is not None:
                        change_data['specified_start_time'].append(change_data[i])
                except:
                    pass

            list_specified_end_time = change_data['list_specified_end_time']
            list_specified_end_time_splitted = list_specified_end_time.split(",")
            list_specified_end_time_splitted = list(dict.fromkeys(list_specified_end_time_splitted))
            list_specified_end_time_removed = change_data['list_specified_end_time_removed']
            list_specified_end_time_removed_splitted = list_specified_end_time_removed.split(",")
            list_specified_end_time_removed_splitted = list(dict.fromkeys(list_specified_end_time_removed_splitted))
            list_specified_end_time_splitted = [item for item in list_specified_end_time_splitted if
                                                item not in list_specified_end_time_removed_splitted]
            change_data['specified_end_time'] = []
            for i in list_specified_end_time_splitted:
                try:
                    if change_data[i] != '' and change_data[i] is not None:
                        change_data['specified_end_time'].append(change_data[i])
                except:
                    pass

            if change_data['datetime_type'] == 'occasional':
                # None weekly
                change_data['start_date'] = None
                change_data['end_date'] = None
                change_data['day_0'] = None
                change_data['start_time_day_0'] = None
                change_data['end_time_day_0'] = None
                change_data['day_1'] = None
                change_data['start_time_day_1'] = None
                change_data['end_time_day_1'] = None
                change_data['day_2'] = None
                change_data['start_time_day_2'] = None
                change_data['end_time_day_2'] = None
                change_data['day_3'] = None
                change_data['start_time_day_3'] = None
                change_data['end_time_day_3'] = None
                change_data['day_4'] = None
                change_data['start_time_day_4'] = None
                change_data['end_time_day_4'] = None
                change_data['day_5'] = None
                change_data['start_time_day_5'] = None
                change_data['end_time_day_5'] = None
                change_data['day_6'] = None
                change_data['start_time_day_6'] = None
                change_data['end_time_day_6'] = None
        else:
            # None occasional
            change_data['specified_date'] = None
            change_data['specified_start_time'] = None
            change_data['specified_end_time'] = None
        program = models.Program.objects.get(pk=num)
        form = forms.AdminAddProgramForm(change_data, request.FILES, instance=program)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.last_modified_by = request.user
            obj.save()
            is_valid = True
        else:
            specified_date = change_data['specified_date']
            specified_start_time = change_data['specified_start_time']
            specified_end_time = change_data['specified_end_time']
        is_edit = True
        args = {'is_valid': is_valid, 'is_edit': is_edit, 'username': get_user(request), 'program': program,
                'form': form, 'specified_date': specified_date, 'specified_start_time': specified_start_time,
                'specified_end_time': specified_end_time}
        return render(request, 'AdminPanel/admin_program_add_edit.html', args)


@staff_member_required
def AdminProgramDuplicate(request, num):
    try:
        program = models.Program.objects.get(pk=num)
        last_program_pk = models.Program.objects.last().pk
        program.pk = None
        program._state.adding = True
        program.slug = program.slug + str(last_program_pk)
        program.save()
        is_copy = True
        args = {'is_copy': is_copy}
        return render(request, 'AdminPanel/admin_program_duplicate.html', args)
    except:
        is_exist = False
        args = {'is_exist': is_exist}
        return render(request, 'AdminPanel/admin_program_duplicate.html', args)
