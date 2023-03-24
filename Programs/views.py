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
from django.urls import reverse
import requests

from Programs import models, serializers


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
            if program.is_on_planning:
                if program.stream_type == 'audio':
                    if program.audio_platform_type == 'shoutcast':
                        if check_shoutcast_stream_status(program.audio_stats_link):
                            program.is_audio_active = True
                        else:
                            program.is_audio_active = False
                    else:
                        if check_wowza_stream_status(program.audio_stats_link):
                            program.is_audio_active = True
                        else:
                            program.is_audio_active = False
                elif program.stream_type == 'video':
                    if check_wowza_stream_status(program.video_stats_link):
                        program.is_video_active = True
                    else:
                        program.is_video_active = False
                else:
                    # audio
                    if program.audio_platform_type == 'shoutcast':
                        if check_shoutcast_stream_status(program.audio_stats_link):
                            program.is_audio_active = True
                        else:
                            program.is_audio_active = False
                    else:
                        if check_wowza_stream_status(program.audio_stats_link):
                            program.is_audio_active = True
                        else:
                            program.is_audio_active = False
                    # video
                    if check_wowza_stream_status(program.video_stats_link):
                        program.is_video_active = True
                    else:
                        program.is_video_active = False
            else:
                program.is_audio_active = False
                program.is_video_active = False

            program.save()
        return HttpResponse('Status Of Programs is Checked.')

    except:
        return HttpResponse('An <span style="color: #ff0000">Error</span> occurred.')


def check_on_planning(request):
    queryset = models.Program.objects.filter(status='publish')

    try:
        for program in queryset:
            # Start Set_Timestamps
            def set_timestamp_earliest():
                try:
                    if program.datetime_type == 'weekly':
                        program.timestamp_earliest = min(program.timestamps_start_weekly)
                    elif program.datetime_type == 'occasional':
                        program.timestamp_earliest = min(program.timestamps_start_occasional)
                    else:
                        timestamps_weekly_earliest = min(program.timestamps_start_weekly)
                        timestamps_occasional_earliest = min(program.timestamps_start_occasional)
                        program.timestamp_earliest = min(timestamps_weekly_earliest, timestamps_occasional_earliest)
                except:
                    program.timestamp_earliest = 0

            # End Set_Timestamps

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

            set_timestamp_earliest()
            if check_stream_time():
                program.is_on_planning = True
            else:
                program.is_on_planning = False
        return HttpResponse('Programs (On Planning) Checked.')

    except:
        return HttpResponse('An <span style="color: #ff0000">Error</span> occurred.')


def create_programs_json(request):
    queryset = models.Program.objects.filter(status='publish')

    try:
        for program in queryset:
            if program.is_on_planning:
                if program.error_count == 0:
                    if program.is_audio_active is True or program.is_video_active is True:
                        program.isLive = True
                    else:
                        if program.isLive:
                            program.error_count = 1
                elif 0 < program.error_count < 5:
                    if program.is_audio_active is True or program.is_video_active is True:
                        program.error_count = 0
                        program.isLive = True
                    else:
                        program.error_count = program.error_count + 1
                else:
                    program.isLive = False
                    program.error_count = 0
            else:
                program.error_count = 0
                program.isLive = False
                program.send_message = 0
            if program.timestamp_earliest == 0:
                program.status = 'archive'
            program.save()

        # Start Create programs.json
        file = open("static/programs.json", "w+", encoding="utf-8")  # TODO Path
        json_var = urlopen(request.build_absolute_uri(reverse('Programs-api:programs')), timeout=5).read().decode(
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
        json_var = urlopen(request.build_absolute_uri(reverse('Programs-api:programs')), timeout=5).read().decode(
            "utf-8")
        try:
            file.write(json_var)
        finally:
            file.close()
        # End Create programs.json

        return HttpResponse('An <span style="color: #ff0000">Error</span> occurred.')


def send_message_to_channel(request):
    # Send Message On Start and End Program
    """
    on start time - program started
    0 = Program not started
    10 = on start time message sent
    11 = on start time and start program message sent
    """

    def send_message(message):
        url = "https://tapi.bale.ai/939503755:Q5trlNp3vQqhTtgkjBnEB7nKbHtQxlBom3hVqmdC/sendMessage"
        headers = {"Content-Type": "application/json"}
        data = {"chat_id": "@radio_rahh_test", "text": message, "disable_notification": True}
        requests.post(url=url, json=data, headers=headers, timeout=3)
    # Send Message On Start and End Program

    queryset = models.Program.objects.filter(status='publish')

    try:
        for program in queryset:
            if program.is_on_planning:
                if program.send_message == 0:
                    message = f"▶️ برنامه رادیو راه به زودی شروع می شود\n\n*{program.title}*\n{program.date_display}\n{program.time_display}\n📣 {program.description}"
                    send_message(message)
                    program.send_message = 10
                if program.is_audio_active is True or program.is_video_active is True:
                    if program.send_message == 10:
                        if program.stream_type == 'audio':
                            message = f"💡پخش زنده *{program.title}* شروع شد\n\n🔊 صوتی\n\n📶 rahh.ir"
                        elif program.stream_type == 'video':
                            message = f"💡پخش زنده *{program.title}* شروع شد\n\n🖥 تصویری\n\n📶 rahh.ir"
                        else:
                            message = f"💡پخش زنده *{program.title}* شروع شد\n\n🔊 صوتی\n🖥 تصویری\n\n📶 rahh.ir"
                        send_message(message)
                        program.send_message = 11
        return HttpResponse('Messages have been sent.')

    except:
        return HttpResponse('An <span style="color: #ff0000">Error</span> occurred.')


class MenuApi(views.APIView):
    def get(self, request):
        queryset = models.Menu.objects.all().order_by('num_order')
        serializer_data = serializers.MenuSerializer(queryset, many=True)
        serializer = {'menuItems': serializer_data.data}
        return response.Response(serializer, status=status.HTTP_200_OK)


def create_menu_json(request):
    try:
        # Start Create menu.json
        file = open("static/menu.json", "w+", encoding="utf-8")  # TODO Path
        json_var = urlopen(request.build_absolute_uri(reverse('Programs-api:menu')), timeout=5).read().decode("utf-8")
        try:
            file.write(json_var)
        finally:
            file.close()
        # End Create programs.json

        return HttpResponse('menu.json is Created.')

    except:
        return HttpResponse('An <span style="color: #ff0000">Error</span> occurred.')
