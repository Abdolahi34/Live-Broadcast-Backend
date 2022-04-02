from django.shortcuts import render
from django.contrib.auth import get_user
from django.contrib.admin.views.decorators import staff_member_required

from Programs import models

from Admin import forms


@staff_member_required
def Admin(request):
    return render(request, 'Admin/admin_main.html', {'username': get_user(request)})


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
    return render(request, 'Admin/admin_program.html', args)


@staff_member_required
def AdminProgramAdd(request):
    if request.method == 'GET':
        form = forms.AdminProgramForm()
        args = {'username': get_user(request), 'form': form}
        return render(request, 'Admin/admin_program_add.html', args)
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
        return render(request, 'Admin/admin_program_add.html', args)


@staff_member_required
def AdminProgramView(request, num):
    try:
        program = models.Program.objects.get(id=num)
        is_exist = True
        args = {'username': get_user(request), 'program': program, 'is_exist': is_exist}
        return render(request, 'Admin/admin_program_view.html', args)
    except:
        is_exist = False
        args = {'is_exist': is_exist}
        return render(request, 'Admin/admin_program_view.html', args)


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
            return render(request, 'Admin/admin_program_edit.html', args)
        except:
            temp_var = 4
            args = {'temp_var': temp_var}
            return render(request, 'Admin/admin_program_edit.html', args)

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
        return render(request, 'Admin/admin_program_edit.html', args)


@staff_member_required
def AdminDateType(request):
    datetypes = models.DateType.objects.all().order_by('id')
    temp_var = 0
    datetype_id = request.GET.get('del_id')
    if datetype_id is not None:
        temp_var = 1
        try:
            if datetypes.get(id=datetype_id) is not None:
                temp_var = 2
                datetype_to_del = datetypes.get(id=datetype_id)
                datetype_to_del.delete()
        except:
            pass
    if datetypes.count() == 0:
        temp_var = 6
    args = {'datetypes': datetypes, 'username': get_user(request), 'temp_var': temp_var}
    return render(request, 'Admin/admin_datetype.html', args)


@staff_member_required
def AdminDateTypeAdd(request):
    if request.method == 'GET':
        form = forms.AdminDateTypeForm()
        args = {'username': get_user(request), 'form': form}
        return render(request, 'Admin/admin_datetype_add.html', args)
    if request.method == 'POST':
        form = forms.AdminDateTypeForm(request.POST)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'form': form}
        return render(request, 'Admin/admin_datetype_add.html', args)


@staff_member_required
def AdminDateTypeView(request, num):
    try:
        datetype = models.DateType.objects.get(id=num)
        is_exist = True
        args = {'username': get_user(request), 'datetype': datetype, 'is_exist': is_exist}
        return render(request, 'Admin/admin_datetype_view.html', args)
    except:
        is_exist = False
        args = {'is_exist': is_exist}
        return render(request, 'Admin/admin_datetype_view.html', args)


@staff_member_required
def AdminDateTypeEdit(request, num):
    if request.method == 'GET':
        try:
            datetype = models.DateType.objects.get(id=num)
            form = forms.AdminDateTypeForm()
            temp_var = 0
            args = {'username': get_user(request), 'datetype': datetype,
                    'temp_var': temp_var, 'form': form,
                    }
            return render(request, 'Admin/admin_datetype_edit.html', args)
        except:
            temp_var = 4
            args = {'temp_var': temp_var}
            return render(request, 'Admin/admin_datetype_edit.html', args)
    if request.method == 'POST':
        datetype = models.DateType.objects.get(id=request.POST.get('id'))
        form = forms.AdminDateTypeForm(request.POST, instance=datetype)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'datetype': datetype, 'form': form,
                }
        return render(request, 'Admin/admin_datetype_edit.html', args)


@staff_member_required
def AdminStreamType(request):
    streamtypes = models.StreamType.objects.all().order_by('id')
    temp_var = 0
    streamtype_id = request.GET.get('del_id')
    if streamtype_id is not None:
        temp_var = 1
        try:
            if streamtypes.get(id=streamtype_id) is not None:
                temp_var = 2
                streamtype_to_del = streamtypes.get(id=streamtype_id)
                streamtype_to_del.delete()
        except:
            pass
    if streamtypes.count() == 0:
        temp_var = 6
    args = {'streamtypes': streamtypes, 'username': get_user(request), 'temp_var': temp_var}
    return render(request, 'Admin/admin_streamtype.html', args)


@staff_member_required
def AdminStreamTypeAdd(request):
    if request.method == 'GET':
        form = forms.AdminStreamTypeForm()
        args = {'username': get_user(request), 'form': form}
        return render(request, 'Admin/admin_streamtype_add.html', args)
    if request.method == 'POST':
        form = forms.AdminStreamTypeForm(request.POST)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'form': form}
        return render(request, 'Admin/admin_streamtype_add.html', args)


@staff_member_required
def AdminStreamTypeView(request, num):
    try:
        streamtype = models.StreamType.objects.get(id=num)
        is_exist = True
        args = {'username': get_user(request), 'streamtype': streamtype, 'is_exist': is_exist}
        return render(request, 'Admin/admin_streamtype_view.html', args)
    except:
        is_exist = False
        args = {'is_exist': is_exist}
        return render(request, 'Admin/admin_streamtype_view.html', args)


@staff_member_required
def AdminStreamTypeEdit(request, num):
    if request.method == 'GET':
        try:
            streamtype = models.StreamType.objects.get(id=num)
            form = forms.AdminStreamTypeForm()
            temp_var = 0
            args = {'username': get_user(request), 'streamtype': streamtype,
                    'temp_var': temp_var, 'form': form,
                    }
            return render(request, 'Admin/admin_streamtype_edit.html', args)
        except:
            temp_var = 4
            args = {'temp_var': temp_var}
            return render(request, 'Admin/admin_streamtype_edit.html', args)
    if request.method == 'POST':
        streamtype = models.StreamType.objects.get(id=request.POST.get('id'))
        form = forms.AdminStreamTypeForm(request.POST, instance=streamtype)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'streamtype': streamtype, 'form': form,
                }
        return render(request, 'Admin/admin_streamtype_edit.html', args)


@staff_member_required
def AdminVideoContent(request):
    videocontents = models.VideoContent.objects.all().order_by('id')
    temp_var = 0
    videocontent_id = request.GET.get('del_id')
    if videocontent_id is not None:
        temp_var = 1
        try:
            if videocontents.get(id=videocontent_id) is not None:
                temp_var = 2
                videocontent_to_del = videocontents.get(id=videocontent_id)
                videocontent_to_del.delete()
        except:
            pass
    if videocontents.count() == 0:
        temp_var = 6
    args = {'videocontents': videocontents, 'username': get_user(request), 'temp_var': temp_var}
    return render(request, 'Admin/admin_videocontent.html', args)


@staff_member_required
def AdminVideoContentAdd(request):
    if request.method == 'GET':
        form = forms.AdminVideoContentForm()
        args = {'username': get_user(request), 'form': form}
        return render(request, 'Admin/admin_videocontent_add.html', args)
    if request.method == 'POST':
        form = forms.AdminVideoContentForm(request.POST)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'form': form}
        return render(request, 'Admin/admin_videocontent_add.html', args)


@staff_member_required
def AdminVideoContentView(request, num):
    try:
        videocontent = models.VideoContent.objects.get(id=num)
        is_exist = True
        args = {'username': get_user(request), 'videocontent': videocontent, 'is_exist': is_exist}
        return render(request, 'Admin/admin_videocontent_view.html', args)
    except:
        is_exist = False
        args = {'is_exist': is_exist}
        return render(request, 'Admin/admin_videocontent_view.html', args)


@staff_member_required
def AdminVideoContentEdit(request, num):
    if request.method == 'GET':
        try:
            videocontent = models.VideoContent.objects.get(id=num)
            form = forms.AdminVideoContentForm()
            temp_var = 0
            args = {'username': get_user(request), 'videocontent': videocontent,
                    'temp_var': temp_var, 'form': form,
                    }
            return render(request, 'Admin/admin_videocontent_edit.html', args)
        except:
            temp_var = 4
            args = {'temp_var': temp_var}
            return render(request, 'Admin/admin_videocontent_edit.html', args)
    if request.method == 'POST':
        videocontent = models.VideoContent.objects.get(id=request.POST.get('id'))
        form = forms.AdminVideoContentForm(request.POST, instance=videocontent)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'videocontent': videocontent, 'form': form,
                }
        return render(request, 'Admin/admin_videocontent_edit.html', args)


@staff_member_required
def AdminVideoStat(request):
    videostats = models.VideoStat.objects.all().order_by('id')
    temp_var = 0
    videostat_id = request.GET.get('del_id')
    if videostat_id is not None:
        temp_var = 1
        try:
            if videostats.get(id=videostat_id) is not None:
                temp_var = 2
                videostat_to_del = videostats.get(id=videostat_id)
                videostat_to_del.delete()
        except:
            pass
    if videostats.count() == 0:
        temp_var = 6
    args = {'videostats': videostats, 'username': get_user(request), 'temp_var': temp_var}
    return render(request, 'Admin/admin_videostat.html', args)


@staff_member_required
def AdminVideoStatAdd(request):
    if request.method == 'GET':
        form = forms.AdminVideoStatForm()
        args = {'username': get_user(request), 'form': form}
        return render(request, 'Admin/admin_videostat_add.html', args)
    if request.method == 'POST':
        form = forms.AdminVideoStatForm(request.POST)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'form': form}
        return render(request, 'Admin/admin_videostat_add.html', args)


@staff_member_required
def AdminVideoStatView(request, num):
    try:
        videostat = models.VideoStat.objects.get(id=num)
        is_exist = True
        args = {'username': get_user(request), 'videostat': videostat, 'is_exist': is_exist}
        return render(request, 'Admin/admin_videostat_view.html', args)
    except:
        is_exist = False
        args = {'is_exist': is_exist}
        return render(request, 'Admin/admin_videostat_view.html', args)


@staff_member_required
def AdminVideoStatEdit(request, num):
    if request.method == 'GET':
        try:
            videostat = models.VideoStat.objects.get(id=num)
            form = forms.AdminVideoStatForm()
            temp_var = 0
            args = {'username': get_user(request), 'videostat': videostat,
                    'temp_var': temp_var, 'form': form,
                    }
            return render(request, 'Admin/admin_videostat_edit.html', args)
        except:
            temp_var = 4
            args = {'temp_var': temp_var}
            return render(request, 'Admin/admin_videostat_edit.html', args)
    if request.method == 'POST':
        videostat = models.VideoStat.objects.get(id=request.POST.get('id'))
        form = forms.AdminVideoStatForm(request.POST, instance=videostat)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'videostat': videostat, 'form': form,
                }
        return render(request, 'Admin/admin_videostat_edit.html', args)


@staff_member_required
def AdminVoiceContent(request):
    voicecontents = models.VoiceContent.objects.all().order_by('id')
    temp_var = 0
    voicecontent_id = request.GET.get('del_id')
    if voicecontent_id is not None:
        temp_var = 1
        try:
            if voicecontents.get(id=voicecontent_id) is not None:
                temp_var = 2
                program_to_del = voicecontents.get(id=voicecontent_id)
                program_to_del.delete()
        except:
            pass
    if voicecontents.count() == 0:
        temp_var = 6
    args = {'voicecontents': voicecontents, 'username': get_user(request), 'temp_var': temp_var}
    return render(request, 'Admin/admin_voicecontent.html', args)


@staff_member_required
def AdminVoiceContentAdd(request):
    if request.method == 'GET':
        form = forms.AdminVoiceContentForm()
        args = {'username': get_user(request), 'form': form}
        return render(request, 'Admin/admin_voicecontent_add.html', args)
    if request.method == 'POST':
        form = forms.AdminVoiceContentForm(request.POST)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'form': form}
        return render(request, 'Admin/admin_voicecontent_add.html', args)


@staff_member_required
def AdminVoiceContentView(request, num):
    try:
        voicecontent = models.VoiceContent.objects.get(id=num)
        is_exist = True
        args = {'username': get_user(request), 'voicecontent': voicecontent, 'is_exist': is_exist}
        return render(request, 'Admin/admin_voicecontent_view.html', args)
    except:
        is_exist = False
        args = {'is_exist': is_exist}
        return render(request, 'Admin/admin_voicecontent_view.html', args)


@staff_member_required
def AdminVoiceContentEdit(request, num):
    if request.method == 'GET':
        try:
            voicecontent = models.VoiceContent.objects.get(id=num)
            form = forms.AdminVoiceContentForm()
            temp_var = 0
            args = {'username': get_user(request), 'voicecontent': voicecontent,
                    'temp_var': temp_var, 'form': form,
                    }
            return render(request, 'Admin/admin_voicecontent_edit.html', args)
        except:
            temp_var = 4
            args = {'temp_var': temp_var}
            return render(request, 'Admin/admin_voicecontent_edit.html', args)
    if request.method == 'POST':
        voicecontent = models.VoiceContent.objects.get(id=request.POST.get('id'))
        form = forms.AdminVoiceContentForm(request.POST, instance=voicecontent)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'voicecontent': voicecontent, 'form': form,
                }
        return render(request, 'Admin/admin_voicecontent_edit.html', args)


@staff_member_required
def AdminVoiceStat(request):
    voicestats = models.VoiceStat.objects.all().order_by('id')
    temp_var = 0
    voicestat_id = request.GET.get('del_id')
    if voicestat_id is not None:
        temp_var = 1
        try:
            if voicestats.get(id=voicestat_id) is not None:
                temp_var = 2
                voicestat_to_del = voicestats.get(id=voicestat_id)
                voicestat_to_del.delete()
        except:
            pass
    if voicestats.count() == 0:
        temp_var = 6
    args = {'voicestats': voicestats, 'username': get_user(request), 'temp_var': temp_var}
    return render(request, 'Admin/admin_voicestat.html', args)


@staff_member_required
def AdminVoiceStatAdd(request):
    if request.method == 'GET':
        form = forms.AdminVoiceStatForm()
        args = {'username': get_user(request), 'form': form}
        return render(request, 'Admin/admin_voicestat_add.html', args)
    if request.method == 'POST':
        form = forms.AdminVoiceStatForm(request.POST)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'form': form}
        return render(request, 'Admin/admin_voicestat_add.html', args)


@staff_member_required
def AdminVoiceStatView(request, num):
    try:
        voicestat = models.VoiceStat.objects.get(id=num)
        is_exist = True
        args = {'username': get_user(request), 'voicestat': voicestat, 'is_exist': is_exist}
        return render(request, 'Admin/admin_voicestat_view.html', args)
    except:
        is_exist = False
        args = {'is_exist': is_exist}
        return render(request, 'Admin/admin_voicestat_view.html', args)


@staff_member_required
def AdminVoiceStatEdit(request, num):
    if request.method == 'GET':
        try:
            voicestat = models.VoiceStat.objects.get(id=num)
            form = forms.AdminVoiceStatForm()
            temp_var = 0
            args = {'username': get_user(request), 'voicestat': voicestat,
                    'temp_var': temp_var, 'form': form,
                    }
            return render(request, 'Admin/admin_voicestat_edit.html', args)
        except:
            temp_var = 4
            args = {'temp_var': temp_var}
            return render(request, 'Admin/admin_voicestat_edit.html', args)
    if request.method == 'POST':
        voicestat = models.VoiceStat.objects.get(id=request.POST.get('id'))
        form = forms.AdminVoiceStatForm(request.POST, instance=voicestat)
        temp_var = 5
        if form.is_valid():
            form.save()
            temp_var = 3
        args = {'temp_var': temp_var, 'username': get_user(request),
                'voicestat': voicestat, 'form': form,
                }
        return render(request, 'Admin/admin_voicestat_edit.html', args)
