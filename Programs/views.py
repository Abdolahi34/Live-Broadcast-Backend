from django.shortcuts import render
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import get_user
from django.views import View

from rest_framework import views, response, status

from Programs import models, forms, serializers


class ProgramView(views.APIView):
    def get(self, request):
        queryset = models.Program.objects.all().order_by('-date_created')
        serializer = serializers.ProgramSerializer(queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class AddProgram(View):
    @login_required(login_url='Accounts:login')
    @permission_required('Programs.add_program', raise_exception=True)
    def get(self, request):
        form = forms.AddProgramForm()
        if_code = False
        args = {'form': form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/program_add.html', args)

    def post(self, request):
        form = forms.AddProgramForm(request.POST, request.FILES)
        if_code = False
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.created_by = request.user
            form_save.last_modified_by = request.user
            form_save.save()
            if_code = True
        args = {'form': form, 'if_code': if_code, 'username': get_user(request)}
        return render(request, 'Programs/program_add.html', args)

