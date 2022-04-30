'''
from django.shortcuts import render

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import get_user
from django.utils.decorators import method_decorator

from django.views import View
from django.db.models.query_utils import Q
'''

from django.http.response import HttpResponseServerError
from rest_framework import views, response, status

from Programs import models, serializers


class ProgramApi(views.APIView):
    def get(self, request):
        queryset = models.Program.objects.all().filter(status='publish')
        for program in queryset:
            if program.datetime_type == 'weekly':
                program.timestamp_earliest = min(program.timestamps_start_weekly)
            elif program.datetime_type == 'occasional':
                program.timestamp_earliest = min(program.timestamps_start_occasional)
            else:
                timestamps_weekly_earliest = min(program.timestamps_start_weekly)
                timestamps_occasional_earliest = min(program.timestamps_start_occasional)
                program.timestamp_earliest = min(timestamps_weekly_earliest, timestamps_occasional_earliest)
            queryset.filter(pk=program.pk).update(timestamp_earliest=program.timestamp_earliest)
        queryset.order_by('-isLive', 'timestamp_earliest')
        serializer = serializers.ProgramSerializer(queryset, context={'request': request}, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class MenuApi(views.APIView):
    def get(self, request):
        queryset = models.Menu.objects.all().order_by('num_order')
        serializer_data = serializers.MenuSerializer(queryset, context={'request': request}, many=True)
        serializer = {'menuItems': serializer_data.data}
        return response.Response(serializer, status=status.HTTP_200_OK)
