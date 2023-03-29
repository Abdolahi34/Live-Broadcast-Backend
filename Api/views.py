'''
from django.shortcuts import render

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import get_user
from django.utils.decorators import method_decorator

from django.views import View
from django.db.models.query_utils import Q
'''

from rest_framework import views, response, status
import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from django.shortcuts import HttpResponse
from django.http import HttpResponseServerError
from django.urls import reverse
import requests

from Api import models, serializers


class ProgramApi(views.APIView):
    def get(self, request):
        queryset = models.Program.objects.filter(status='publish').order_by('-isLive', 'timestamp_earliest')
        serializer = serializers.ProgramSerializer(queryset, context={'request': request}, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


def check_live(request):
    # Start Check Shoutcast Stream Status
    def check_shoutcast_stream_status(stats_url):
        url_var = urlopen(stats_url, timeout=5)
        # We're at the root node (<main tag>)
        root_node = ET.parse(url_var).getroot()
        # Find interested in tag
        shoutcast_status = root_node.find('STREAMSTATUS').text
        return int(shoutcast_status)

    # End Check Shoutcast Stream Status

    # Start Check Wowza Stream Status
    def check_wowza_stream_status(stats_url):
        url_var = urlopen(stats_url, timeout=5)
        # We're at the root node (<main tag>)
        root_node = ET.parse(url_var).getroot()
        # We need to go one level below to get (interested in tag)
        i = 1
        for tag in root_node.findall('ConnectionCount/'):
            # Get the value of the heading attribute
            if i == 3:
                wowza_status = tag.text
                return int(wowza_status)
            i += 1

    # End Check Wowza Stream Status

    queryset = models.Program.objects.filter(status='publish')

    try:
        for program in queryset:
            # Start Check Time of Stream
            def check_stream_time():
                def check_timestamp(start_timestamp, end_timestamp):
                    obj_len = len(start_timestamp)
                    for i in range(obj_len):
                        if start_timestamp[i] <= now_timestamp:
                            if now_timestamp < end_timestamp[i]:
                                return True
                    return False

                now_timestamp = datetime.datetime.now().timestamp()
                if program.datetime_type == 'weekly':
                    if check_timestamp(program.timestamps_start_weekly, program.timestamps_end_weekly):
                        return True
                    else:
                        return False
                elif program.datetime_type == 'occasional':
                    if check_timestamp(program.timestamps_start_occasional, program.timestamps_end_occasional):
                        return True
                    else:
                        return False
                else:
                    if check_timestamp(program.timestamps_start_weekly,
                                       program.timestamps_end_weekly) or check_timestamp(
                        program.timestamps_start_occasional, program.timestamps_end_occasional):
                        return True
                    else:
                        return False

            # End Check Time of Stream

            if check_stream_time():
                if program.stream_type == 'audio':
                    if program.audio_platform_type == 'shoutcast':
                        if check_shoutcast_stream_status(program.audio_stats_link):
                            program.is_audio_active = True
                            program.isLive = True
                        else:
                            program.is_audio_active = False
                            program.isLive = False
                    else:
                        if check_wowza_stream_status(program.audio_stats_link):
                            program.is_audio_active = True
                            program.isLive = True
                        else:
                            program.is_audio_active = False
                            program.isLive = False
                elif program.stream_type == 'video':
                    if check_wowza_stream_status(program.video_stats_link):
                        program.is_video_active = True
                        program.isLive = True
                    else:
                        program.is_video_active = False
                        program.isLive = False
                else:
                    # audio
                    if program.audio_platform_type == 'shoutcast':
                        if check_shoutcast_stream_status(program.audio_stats_link):
                            program.is_audio_active = True
                            program.isLive = True
                        else:
                            program.is_audio_active = False
                            program.isLive = False
                    else:
                        if check_wowza_stream_status(program.audio_stats_link):
                            program.is_audio_active = True
                            program.isLive = True
                        else:
                            program.is_audio_active = False
                            program.isLive = False
                    # video
                    if check_wowza_stream_status(program.video_stats_link):
                        program.is_video_active = True
                        program.isLive = True
                    else:
                        program.is_video_active = False
                        program.isLive = False
            else:
                program.is_audio_active = False
                program.is_video_active = False
                program.isLive = False

            program.save()
        return HttpResponse('live status is Checked.')
    except:
        return HttpResponseServerError()


def create_programs_json(request):
    queryset = models.Program.objects.filter(status='publish')

    try:
        for program in queryset:
            # Start Check Time of Stream
            def check_stream_time():
                def check_timestamp(start_timestamp, end_timestamp):
                    obj_len = len(start_timestamp)
                    for i in range(obj_len):
                        if start_timestamp[i] <= now_timestamp:
                            if now_timestamp < end_timestamp[i]:
                                return True
                    return False

                now_timestamp = datetime.datetime.now().timestamp()
                if program.datetime_type == 'weekly':
                    if check_timestamp(program.timestamps_start_weekly, program.timestamps_end_weekly):
                        return True
                    else:
                        return False
                elif program.datetime_type == 'occasional':
                    if check_timestamp(program.timestamps_start_occasional, program.timestamps_end_occasional):
                        return True
                    else:
                        return False
                else:
                    if check_timestamp(program.timestamps_start_weekly,
                                       program.timestamps_end_weekly) or check_timestamp(
                        program.timestamps_start_occasional, program.timestamps_end_occasional):
                        return True
                    else:
                        return False

            # End Check Time of Stream

            # Start Set_Timestamps
            def set_timestamp_earliest():
                def set_outdated_program():
                    program.timestamp_earliest = 0
                    program.status = 'archive'

                if program.datetime_type == 'weekly':
                    try:
                        program.timestamp_earliest = min(program.timestamps_start_weekly)
                    except:
                        set_outdated_program()
                elif program.datetime_type == 'occasional':
                    try:
                        program.timestamp_earliest = min(program.timestamps_start_occasional)
                    except:
                        set_outdated_program()
                else:
                    try:
                        timestamps_weekly_earliest = min(program.timestamps_start_weekly)
                        timestamps_occasional_earliest = min(program.timestamps_start_occasional)
                        program.timestamp_earliest = min(timestamps_weekly_earliest, timestamps_occasional_earliest)
                    except:
                        if not program.timestamps_start_weekly and not program.timestamps_start_occasional:
                            set_outdated_program()
                        else:
                            if not program.timestamps_start_weekly:
                                program.timestamp_earliest = min(program.timestamps_start_occasional)
                            else:
                                program.timestamp_earliest = min(program.timestamps_start_weekly)

            # End Set_Timestamps

            set_timestamp_earliest()
            if check_stream_time():
                error_count = program.error_count
                if error_count == 0:
                    if program.is_audio_active is True or program.is_video_active is True:
                        program.isLive = True
                    else:
                        if program.isLive:
                            program.error_count = 1
                elif 0 < error_count < 5:
                    if program.is_audio_active is True or program.is_video_active is True:
                        program.error_count = 0
                    else:
                        program.error_count = error_count + 1
                elif error_count == 5:
                    program.isLive = False
                    program.error_count = 0
            if program.timestamp_earliest == 0:
                program.status = 'archive'
            program.save()

        # Start Create programs.json
        file = open("static/programs.json", "w+", encoding="utf-8")  # TODO Path
        json_var = urlopen(request.build_absolute_uri(reverse('Api:programs')), timeout=5).read().decode(
            "utf-8")
        try:
            file.write(json_var)
        finally:
            file.close()
        # End Create programs.json

        return HttpResponse('programs.json is Created.')

    except:
        for program in queryset:
            if program.stream_type == 'audio':
                program.is_audio_active = True
                program.is_video_active = False
            elif program.stream_type == 'video':
                program.is_audio_active = False
                program.is_video_active = True
            else:
                program.is_audio_active = True
                program.is_video_active = True
            program.isLive = False
            program.error_count = 0

            program.save()

        # Start Create programs.json
        file = open("static/programs.json", "w+", encoding="utf-8")  # TODO Path
        json_var = urlopen(request.build_absolute_uri(reverse('Api:programs')), timeout=5).read().decode(
            "utf-8")
        try:
            file.write(json_var)
        finally:
            file.close()
        # End Create programs.json

        return HttpResponseServerError()


class MenuApi(views.APIView):
    def get(self, request):
        queryset = models.Menu.objects.all().order_by('num_order')
        serializer_data = serializers.MenuSerializer(queryset, many=True)
        serializer = {'menuItems': serializer_data.data}
        return response.Response(serializer, status=status.HTTP_200_OK)


def create_menu_json(request):
    # Start Create menu.json
    file = open("static/menu.json", "w+", encoding="utf-8")  # TODO Path
    json_var = urlopen(request.build_absolute_uri(reverse('Api:menu')), timeout=5).read().decode("utf-8")
    try:
        file.write(json_var)
    finally:
        file.close()
    # End Create programs.json

    return HttpResponse('menu.json is Created.')


def every_10_second(request):
    try:
        check_live_status_code = requests.get('https://radio-api.rahh.ir/api/v1/check-live/').status_code
        create_programs_json_status_code = requests.get(
            'https://radio-api.rahh.ir/api/v1/create-programs-json/').status_code
        create_menu_json_status_code = requests.get('https://radio-api.rahh.ir/api/v1/create-menu-json/').status_code
        if check_live_status_code != 200 or create_programs_json_status_code != 200 or create_menu_json_status_code != 200:
            return HttpResponseServerError()
        return HttpResponse('Everything was done successfully.')
    except:
        return HttpResponseServerError()
