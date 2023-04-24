from django.shortcuts import render
from django.contrib.auth import get_user
from django.contrib.admin.views.decorators import staff_member_required
import os
import logging

from api import models

from admin_panel import forms


@staff_member_required
def Admin(request):
    programs_publish = models.Program.objects.filter(status='publish').count()
    programs_draft = models.Program.objects.filter(status='draft').count()
    programs_archive = models.Program.objects.filter(status='archive').count()
    programs_live = models.Program.objects.filter(status='publish', isLive=True).count()
    args = {'username': get_user(request), 'programs_publish': programs_publish, 'programs_draft': programs_draft,
            'programs_archive': programs_archive, 'programs_live': programs_live}
    return render(request, 'admin_panel/admin_main.html', args)


@staff_member_required
def AdminProgram(request):
    programs = models.Program.objects.order_by('-status', 'timestamp_earliest')
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
            logging.exception('The try block part encountered an error.')
            is_exist = False
    program_null = False
    if programs.count() == 0:
        program_null = True
    args = {'programs': programs, 'username': get_user(request), 'is_exist': is_exist, 'is_deleted': is_deleted,
            'program_null': program_null}
    return render(request, 'admin_panel/admin_program.html', args)


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
        return render(request, 'admin_panel/admin_program_add_edit.html', args)
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
                    logging.exception('The try block part encountered an error.')

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
                    logging.exception('The try block part encountered an error.')

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
                    logging.exception('The try block part encountered an error.')

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
        if change_data['stream_type'] == 'audio':
            change_data['video_link'] = None
            change_data['video_stats_link'] = None
            change_data['video_platform_type'] = None
        elif change_data['stream_type'] == 'video':
            change_data['audio_link'] = None
            change_data['audio_stats_link'] = None
            change_data['audio_platform_type'] = None
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
        return render(request, 'admin_panel/admin_program_add_edit.html', args)


@staff_member_required
def AdminProgramView(request, num):
    try:
        program = models.Program.objects.get(pk=num)
        is_exist = True
        args = {'username': get_user(request), 'program': program, 'is_exist': is_exist}
        return render(request, 'admin_panel/admin_program_view.html', args)
    except:
        logging.exception('The try block part encountered an error.')
        return render(request, 'admin_panel/admin_program_does_not_exist.html')


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
            return render(request, 'admin_panel/admin_program_add_edit.html', args)
        except:
            logging.exception('The try block part encountered an error.')
            return render(request, 'admin_panel/admin_program_does_not_exist.html')

    if request.method == 'POST':
        is_valid = False
        specified_date = None
        specified_start_time = None
        specified_end_time = None
        program = models.Program.objects.get(pk=num)
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
                    logging.exception('The try block part encountered an error.')

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
                    logging.exception('The try block part encountered an error.')

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
                    logging.exception('The try block part encountered an error.')

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
        if change_data['stream_type'] == 'audio':
            change_data['video_link'] = None
            change_data['video_stats_link'] = None
            change_data['video_platform_type'] = None
        elif change_data['stream_type'] == 'video':
            change_data['audio_link'] = None
            change_data['audio_stats_link'] = None
            change_data['audio_platform_type'] = None

        form = forms.AdminAddProgramForm(change_data, request.FILES, instance=program)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.last_modified_by = request.user

            send_logo = False
            send_player_background = False
            # set logo and player_background
            # logo has sent
            try:
                if change_data['logo'] != '':
                    pass
                else:
                    # logo doesn't send
                    # set before logo
                    obj.logo = program.logo
                    send_logo = False
            except:
                logging.exception('The try block part encountered an error.')
                send_logo = True
            if program.stream_type != 'video':
                # player_background has sent
                try:
                    if change_data['player_background'] != '':
                        pass
                    else:
                        # player_background doesn't send
                        # set before player_background
                        obj.player_background = program.player_background
                        send_player_background = False
                except:
                    logging.exception('The try block part encountered an error.')
                    send_player_background = True
            # End set logo and player_background

            program = models.Program.objects.get(pk=num)

            # remove old logo and player_background
            # remove old logo if new logo is sent
            if send_logo:
                logo_path = program.logo.path
                if os.path.exists(logo_path):
                    os.remove(logo_path)
            # remove old player_background if new player_background is sent
            if send_player_background:
                player_background_path = program.player_background.path
                if os.path.exists(player_background_path):
                    os.remove(player_background_path)
            # End remove old logo and player_background
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
        return render(request, 'admin_panel/admin_program_add_edit.html', args)


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
        return render(request, 'admin_panel/admin_program_duplicate.html', args)
    except:
        logging.exception('The try block part encountered an error.')
        return render(request, 'admin_panel/admin_program_does_not_exist.html')
