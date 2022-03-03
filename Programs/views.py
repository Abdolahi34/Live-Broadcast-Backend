from django.shortcuts import render

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import get_user
from django.utils.decorators import method_decorator

from django.views import View
from django.db.models.query_utils import Q

from rest_framework import views, response, status

from Programs import models, forms, serializers


class ProgramApi(views.APIView):
    def get(self, request):
        queryset = models.Program.objects.filter(is_active=True).order_by('num_order')
        serializer = serializers.ProgramSerializer(queryset, context={'request': request}, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(login_required(login_url='Accounts:login'), name='dispatch')
@method_decorator(permission_required('Programs.add_program', raise_exception=True), name='dispatch')
class AddProgramView(View):
    def get(self, request):
        program_form = forms.AddProgramForm()
        if_code = False
        args = {'program_form': program_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/program_add.html', args)

    def post(self, request):
        program_form = forms.AddProgramForm(request.POST, request.FILES)
        if_code = False
        if program_form.is_valid():
            form = program_form.save(commit=False)
            form.created_by = request.user
            form.last_modified_by = request.user
            form = program_form.save()
            if_code = True
        args = {'program_form': program_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/program_add.html', args)


@method_decorator(login_required(login_url='Accounts:login'), name='dispatch')
@method_decorator(permission_required('Programs.add_program', raise_exception=True), name='dispatch')
class AddStreamTypeView(View):
    def get(self, request):
        stream_type_form = forms.AddStreamTypeForm()
        if_code = False
        args = {'stream_type_form': stream_type_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/stream_type_add.html', args)

    def post(self, request):
        stream_type_form = forms.AddStreamTypeForm(request.POST)
        if_code = False
        if stream_type_form.is_valid():
            form = stream_type_form.save()
            if_code = True
        args = {'stream_type_form': stream_type_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/stream_type_add.html', args)


@method_decorator(login_required(login_url='Accounts:login'), name='dispatch')
@method_decorator(permission_required('Programs.add_program', raise_exception=True), name='dispatch')
class AddVideoContentView(View):
    def get(self, request):
        video_content_form = forms.AddVideoContentForm()
        if_code = False
        args = {'video_content_form': video_content_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/video_content_add.html', args)

    def post(self, request):
        video_content_form = forms.AddVideoContentForm(request.POST)
        if_code = False
        if video_content_form.is_valid():
            form = video_content_form.save()
            if_code = True
        args = {'video_content_form': video_content_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/video_content_add.html', args)


@method_decorator(login_required(login_url='Accounts:login'), name='dispatch')
@method_decorator(permission_required('Programs.add_program', raise_exception=True), name='dispatch')
class AddVideoStatView(View):
    def get(self, request):
        video_stat_form = forms.AddVideoStatForm()
        if_code = False
        args = {'video_stat_form': video_stat_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/video_stat_add.html', args)

    def post(self, request):
        video_stat_form = forms.AddVideoStatForm(request.POST)
        if_code = False
        if video_stat_form.is_valid():
            form = video_stat_form.save()
            if_code = True
        args = {'video_stat_form': video_stat_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/video_stat_add.html', args)


@method_decorator(login_required(login_url='Accounts:login'), name='dispatch')
@method_decorator(permission_required('Programs.add_program', raise_exception=True), name='dispatch')
class AddVoiceContentView(View):
    def get(self, request):
        voice_content_form = forms.AddVoiceContentForm()
        if_code = False
        args = {'voice_content_form': voice_content_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/voice_content_add.html', args)

    def post(self, request):
        voice_content_form = forms.AddVoiceContentForm(request.POST)
        if_code = False
        if voice_content_form.is_valid():
            form = voice_content_form.save()
            if_code = True
        args = {'voice_content_form': voice_content_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/voice_content_add.html', args)


@method_decorator(login_required(login_url='Accounts:login'), name='dispatch')
@method_decorator(permission_required('Programs.add_program', raise_exception=True), name='dispatch')
class AddVoiceStatView(View):
    def get(self, request):
        voice_stat_form = forms.AddVoiceStatForm()
        if_code = False
        args = {'voice_stat_form': voice_stat_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/voice_stat_add.html', args)

    def post(self, request):
        voice_stat_form = forms.AddVoiceStatForm(request.POST)
        if_code = False
        if voice_stat_form.is_valid():
            form = voice_stat_form.save()
            if_code = True
        args = {'voice_stat_form': voice_stat_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/voice_stat_add.html', args)


@method_decorator(login_required(login_url='Accounts:login'), name='dispatch')
@method_decorator(permission_required('Programs.add_program', raise_exception=True), name='dispatch')
class AddDateTypeView(View):
    def get(self, request):
        date_type_form = forms.AddDateTypeForm()
        if_code = False
        args = {'date_type_form': date_type_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/date_type_add.html', args)

    def post(self, request):
        date_type_form = forms.AddDateTypeForm(request.POST)
        if_code = False
        if date_type_form.is_valid():
            form = date_type_form.save()
            if_code = True
        args = {'date_type_form': date_type_form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/date_type_add.html', args)


@method_decorator(login_required(login_url='Accounts:login'), name='dispatch')
@method_decorator(permission_required('Programs.delete_program', raise_exception=True), name='dispatch')
class DeleteProgramView(View):
    def get(self, request):
        return render(request, 'Programs/delete_program.html')

    def post(self, request):
        programs = models.Program.objects
        search_value = request.POST['search_value']
        selected_programs = programs.filter(Q(title__contains=search_value) | Q(slug__contains=search_value))
        if_code = 1
        query_list = list(selected_programs)
        if query_list == []:
            if_code = 2
        args = {'selected_programs': selected_programs, 'if_code': if_code}
        return render(request, 'Programs/delete_program.html', args)


@method_decorator(login_required(login_url='Accounts:login'), name='dispatch')
@method_decorator(permission_required('Programs.delete_program', raise_exception=True), name='dispatch')
class ProgramViewBeforeDelete(View):
    def get(self, request, slug):
        try:
            program = models.Program.objects.get(slug=slug)
            if_code = 1
            args = {'program': program, 'if_code': if_code}
            return render(request, 'Programs/view_program_before_delete.html', args)
        except:
            if_code = 2
            args = {'if_code': if_code}
            return render(request, 'Programs/view_program_before_delete.html', args)

    def post(self, request, slug):
        program = models.Program.objects.get(slug=slug)
        program.delete()
        if_code = 3
        args = {'if_code': if_code}
        return render(request, 'Programs/view_program_before_delete.html', args)
