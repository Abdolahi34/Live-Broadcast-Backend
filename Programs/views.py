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
import requests

from Programs import models, serializers


class ProgramApi(views.APIView):
    def get(self, request):
        try:
            queryset = models.Program.objects.all()

            # Specify started and unstarted programs
            for program in queryset:
                def check_wowza_status(stream_type):
                    if stream_type == 'audio':
                        voice_stats_text = requests.get('https://live.mostadrak.org/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/masjed/monitoring/current').text
                        voice_stream_status = voice_stats_text[voice_stats_text.find('<string>RTMP') + 34]
                        if voice_stream_status != '0':
                            queryset.filter(id=program.id).update(isLive=True)
                        else:
                            queryset.filter(id=program.id).update(isLive=False)
                            queryset.filter(id=program.id).update(voice_link='')
                            queryset.filter(id=program.id).update(voice_stats_link='')
                            queryset.filter(id=program.id).update(title_in_player='برنامه شروع نشده است')
                    else:
                        video_stats_text = requests.get('https://live.mostadrak.org/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/masjed/monitoring/current').text
                        video_stream_status = video_stats_text[video_stats_text.find('<string>RTMP') + 34]
                        if video_stream_status != '0':
                            queryset.filter(id=program.id).update(isLive=True)
                        else:
                            queryset.filter(id=program.id).update(isLive=False)
                            queryset.filter(id=program.id).update(video_link='')
                            queryset.filter(id=program.id).update(video_stats_link='')
                            queryset.filter(id=program.id).update(title_in_player='برنامه شروع نشده است')

                # Live audio player
                if program.voice_stats_type == 'shoutcast':
                    voice_stats_text = requests.get('https://radio.masjedsafa.com/stats?sid=2').text
                    voice_stream_status = int(voice_stats_text[voice_stats_text.find('<STREAMSTATUS>') + 14])
                    if voice_stream_status:
                        queryset.filter(id=program.id).update(isLive=True)
                    else:
                        queryset.filter(id=program.id).update(isLive=False)
                        queryset.filter(id=program.id).update(voice_link='')
                        queryset.filter(id=program.id).update(voice_stats_link='')
                        queryset.filter(id=program.id).update(title_in_player='برنامه شروع نشده است')
                else:
                    check_wowza_status('audio')

                # Live video player
                check_wowza_status('video')

            queryset.order_by('isLive')
            serializer = serializers.ProgramSerializer(queryset, context={'request': request}, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return HttpResponseServerError()


class MenuApi(views.APIView):
    def get(self, request):
        queryset = models.Menu.objects.all().order_by('num_order')
        serializer = serializers.MenuSerializer(queryset, context={'request': request}, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

