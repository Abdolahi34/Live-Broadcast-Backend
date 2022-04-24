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
import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlopen

from Programs import models, serializers


class ProgramApi(views.APIView):
    def get(self, request):
        try:
            queryset = models.Program.objects.all().filter(status='publish')

            # Specify started and unstarted programs
            for program in queryset:
                # Start Check_Stats_Status
                def check_stats_status():
                    if program.voice_stats_type == 'shoutcast':
                        url_var = urlopen('https://radio.masjedsafa.com/stats?sid=2')
                        # We're at the root node (<main tag>)
                        root_node = ET.parse(url_var).getroot()
                        # Find interested in tag
                        voice_stream_status = root_node.find('STREAMSTATUS').text
                        if voice_stream_status == '1':
                            queryset.filter(pk=program.pk).update(is_voice_active=True)
                            program.is_voice_active = True
                        else:
                            queryset.filter(pk=program.pk).update(is_voice_active=False)
                            program.is_voice_active = False
                    if program.voice_stats_type is not None or program.video_stats_type is not None:
                        url_var = urlopen(
                            'https://live.mostadrak.org/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/masjed/monitoring/current')
                        # We're at the root node (<main tag>)
                        root_node = ET.parse(url_var).getroot()
                        # We need to go one level below to get (interested in tag)
                        i = 0
                        for tag in root_node.findall('ConnectionCount/entry/long'):
                            # Get the value of the heading attribute
                            i += 1
                            if i == 3:
                                stream_status = tag.text
                                break
                        if program.voice_stats_type == 'wowza':
                            if stream_status == '1':
                                queryset.filter(pk=program.pk).update(is_voice_active=True)
                                program.is_voice_active = True
                            else:
                                queryset.filter(pk=program.pk).update(is_voice_active=False)
                                program.is_voice_active = False
                        if program.video_stats_type == 'wowza':
                            if stream_status == '1':
                                queryset.filter(pk=program.pk).update(is_video_active=True)
                                program.is_video_active = True
                            else:
                                queryset.filter(pk=program.pk).update(is_video_active=False)
                                program.is_video_active = False

                check_stats_status()
                # End Check_Stats_Status

                # Start Check_Time_of_Stream
                def check_stream_time():
                    """
                    در تقویم میلادی منظور از کد 0 یکشنبه می باشد.
                    در تقویم شمسی منظور از کد 0 شنبه می باشد.
                    """
                    if program.regularly == 'daily':
                        if start_regular_timestamp <= base_datetime.now().timestamp() <= end_regular_timestamp:
                            return True
                        else:
                            return False
                    if program.regularly == 'weekly':
                        now_weekday = datetime.datetime.now().isoweekday()
                        if program.day_0:
                            if now_weekday == 6:
                                if start_regular_timestamp <= base_datetime.now().timestamp() <= end_regular_timestamp:
                                    return True
                                else:
                                    return False
                        if program.day_1:
                            if now_weekday == 0:
                                if start_regular_timestamp <= base_datetime.now().timestamp() <= end_regular_timestamp:
                                    return True
                                else:
                                    return False
                        if program.day_2:
                            if now_weekday == 1:
                                if start_regular_timestamp <= base_datetime.now().timestamp() <= end_regular_timestamp:
                                    return True
                                else:
                                    return False
                        if program.day_3:
                            if now_weekday == 2:
                                if start_regular_timestamp <= base_datetime.now().timestamp() <= end_regular_timestamp:
                                    return True
                                else:
                                    return False
                        if program.day_4:
                            if now_weekday == 3:
                                if start_regular_timestamp <= base_datetime.now().timestamp() <= end_regular_timestamp:
                                    return True
                                else:
                                    return False
                        if program.day_5:
                            if now_weekday == 4:
                                if start_regular_timestamp <= base_datetime.now().timestamp() <= end_regular_timestamp:
                                    return True
                                else:
                                    return False
                        if program.day_6:
                            if now_weekday == 5:
                                if start_regular_timestamp <= base_datetime.now().timestamp() <= end_regular_timestamp:
                                    return True
                                else:
                                    return False
                    # TODO
                    if program.datetime_type == 'occasional':
                        for specified_date in program.specified_date:
                            if base_datetime.now().date() == specified_date:
                                return True

                if program.is_voice_active or program.is_video_active:
                    base_datetime = datetime.datetime

                    if program.datetime_type == 'regular':
                        start_regular_timestamp = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                                base_datetime.now().day, program.start_time.hour,
                                                                program.start_time.minute, program.start_time.second,
                                                                0).timestamp()
                        end_regular_timestamp = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                              base_datetime.now().day, program.end_time.hour,
                                                              program.end_time.minute, program.end_time.second,
                                                              0).timestamp()
                        if end_regular_timestamp < start_regular_timestamp:
                            end_regular_timestamp = end_regular_timestamp + 86400
                            # 86400 s = 1 day

                    queryset.filter(pk=program.pk).update(isLive=check_stream_time())
                # End Check_Time_of_Stream

            queryset.order_by('-isLive')
            serializer = serializers.ProgramSerializer(queryset, context={'request': request}, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return HttpResponseServerError()


class MenuApi(views.APIView):
    def get(self, request):
        try:
            queryset = models.Menu.objects.all().order_by('num_order')
            serializer_data = serializers.MenuSerializer(queryset, context={'request': request}, many=True)
            serializer = {'menuItems': serializer_data.data}
            return response.Response(serializer, status=status.HTTP_200_OK)
        except:
            return HttpResponseServerError()
