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
import logging

from api import models, serializers

logger = logging.getLogger(__name__)


class ProgramApi(views.APIView):
    def get(self, request):
        queryset = models.Program.objects.filter(status='publish').order_by('-isLive', 'timestamp_earliest')
        serializer = serializers.ProgramSerializer(queryset, context={'request': request}, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


# Every 10 Sec
def check_on_planning(request):
    queryset = models.Program.objects.filter(status='publish')
    try:
        for program in queryset:
            # Start Check Time of Stream
            def check_stream_time():
                def check_timestamp(start_timestamp, end_timestamp):
                    try:
                        obj_len = len(start_timestamp)
                        for i in range(obj_len):
                            if start_timestamp[i] <= now_timestamp:
                                if now_timestamp < end_timestamp[i]:
                                    return True
                        return False
                    except Exception as e:
                        logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
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
                program.is_on_planning = True
            else:
                program.is_on_planning = False
            program.save()
        return HttpResponse('Programs (On Planning) Checked.')

    except Exception as e:
        logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
        return HttpResponseServerError('Internal Server Error')


# Every 10 Sec
def check_live(request):
    # Start Check Shoutcast Stream Status
    # TODO Check based on shoutcast version
    def check_shoutcast_stream_status(stats_url):
        url_var = urlopen(stats_url, timeout=5)
        # We're at the root node (<main tag>)
        root_node = ET.parse(url_var).getroot()
        # Find interested in tag
        shoutcast_status = root_node.find('STREAMSTATUS').text
        return int(shoutcast_status)

    # End Check Shoutcast Stream Status

    # Start Check Wowza Stream Status
    # TODO Check based on wowza version
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

    except Exception as e:
        logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
        return HttpResponseServerError('Internal Server Error')


# programs.json will be created automatically.
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
                    else:
                        program.error_count = program.error_count + 1
                else:
                    program.error_count = 0
                    program.isLive = False
            else:
                program.error_count = 0
                program.isLive = False
            program.save()

        # Start Create programs.json
        file = open("static/programs.json", "w+", encoding="utf-8")  # TODO Path
        json_var = urlopen(request.build_absolute_uri(reverse('api:programs')), timeout=5).read().decode("utf-8")
        try:
            file.write(json_var)
        except Exception as e:
            logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
        finally:
            file.close()
        # End Create programs.json
        return HttpResponse('programs.json is Created.')

    except Exception as e:
        logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
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
        json_var = urlopen(request.build_absolute_uri(reverse('api:programs')), timeout=5).read().decode("utf-8")
        try:
            file.write(json_var)
        except Exception as e:
            logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
        finally:
            file.close()
        # End Create programs.json
        return HttpResponseServerError('Internal Server Error')


# TODO Synchronize the set_timestamps function with the save function of the Program model.
# Every day
def set_timestamps(request):
    try:
        queryset = models.Program.objects.filter(status='publish')
        for program in queryset:
            def timestamps_weekly_func():
                def append_days_timestamps_func(start_date, start_time, end_time):
                    while start_date <= program.end_date:
                        this_timestamp_start = datetime.datetime(start_date.year, start_date.month, start_date.day,
                                                                 start_time.hour, start_time.minute,
                                                                 start_time.second, 0).timestamp()
                        if start_time < end_time:
                            this_timestamp_end = datetime.datetime(start_date.year, start_date.month, start_date.day,
                                                                   end_time.hour, end_time.minute,
                                                                   end_time.second, 0).timestamp()
                        else:
                            # start_time before 12 pm and end_time after 12 pm
                            start_date += datetime.timedelta(days=1)
                            this_timestamp_end = datetime.datetime(start_date.year, start_date.month, start_date.day,
                                                                   end_time.hour, end_time.minute,
                                                                   end_time.second, 0).timestamp()
                            start_date -= datetime.timedelta(days=1)
                        program.timestamps_start_weekly.append(this_timestamp_start)
                        program.timestamps_end_weekly.append(this_timestamp_end)
                        start_date += datetime.timedelta(days=7)

                days = [program.day_0, program.day_1, program.day_2, program.day_3, program.day_4, program.day_5,
                        program.day_6]
                start_time_days = [program.start_time_day_0, program.start_time_day_1, program.start_time_day_2,
                                   program.start_time_day_3, program.start_time_day_4, program.start_time_day_5,
                                   program.start_time_day_6]
                end_time_days = [program.end_time_day_0, program.end_time_day_1, program.end_time_day_2,
                                 program.end_time_day_3, program.end_time_day_4, program.end_time_day_5,
                                 program.end_time_day_6]

                now_date = datetime.datetime.now().date()
                if now_date <= program.start_date:
                    for i in range(7):
                        if days[i]:
                            append_days_timestamps_func(program.start_date, start_time_days[i], end_time_days[i])
                elif now_date <= program.end_date:
                    now_weekday = datetime.datetime.now().weekday()
                    iso_weekday_nums = [5, 6, 0, 1, 2, 3, 4]
                    for i in range(7):
                        if days[i]:
                            if now_weekday == iso_weekday_nums[i]:
                                append_days_timestamps_func(now_date, start_time_days[i], end_time_days[i])
                            else:
                                now_date += datetime.timedelta(days=now_weekday - iso_weekday_nums[i])
                                append_days_timestamps_func(now_date, start_time_days[i], end_time_days[i])
                                now_date -= datetime.timedelta(days=now_weekday - iso_weekday_nums[i])

            def timestamps_occasional_func():
                try:
                    program_len = len(program.specified_date)
                    for i in range(program_len):
                        this_specified_date = program.specified_date[i]
                        if datetime.datetime.now().date() <= this_specified_date:
                            this_specified_start_time = program.specified_start_time[i]
                            this_specified_end_time = program.specified_end_time[i]
                            this_timestamp_start = datetime.datetime(this_specified_date.year,
                                                                     this_specified_date.month,
                                                                     this_specified_date.day,
                                                                     this_specified_start_time.hour,
                                                                     this_specified_start_time.minute,
                                                                     this_specified_start_time.second, 0).timestamp()
                            # start_time before 12 pm and end_time after 12 pm
                            if this_specified_end_time < this_specified_start_time:
                                this_specified_date += datetime.timedelta(days=1)
                            this_timestamp_end = datetime.datetime(this_specified_date.year, this_specified_date.month,
                                                                   this_specified_date.day,
                                                                   this_specified_end_time.hour,
                                                                   this_specified_end_time.minute,
                                                                   this_specified_end_time.second, 0).timestamp()
                            program.timestamps_start_occasional.append(this_timestamp_start)
                            program.timestamps_end_occasional.append(this_timestamp_end)
                except Exception as e:
                    logger.error('The try block part encountered an error: %s', str(e), exc_info=True)

            if program.datetime_type == 'weekly':
                # set occasional timestamps None
                program.timestamps_start_occasional = None
                program.timestamps_end_occasional = None
                # set weekly timestamps
                program.timestamps_start_weekly = []
                program.timestamps_end_weekly = []
                timestamps_weekly_func()
            elif program.datetime_type == 'occasional':
                # set weekly timestamps None
                program.timestamps_start_weekly = None
                program.timestamps_end_weekly = None
                # set occasional timestamps
                program.timestamps_start_occasional = []
                program.timestamps_end_occasional = []
                timestamps_occasional_func()
            else:
                program.timestamps_start_weekly = []
                program.timestamps_end_weekly = []
                timestamps_weekly_func()
                program.timestamps_start_occasional = []
                program.timestamps_end_occasional = []
                timestamps_occasional_func()

            # Start Set_Timestamp_Earliest
            def set_outdated_program():
                program.timestamp_earliest = 0
                program.status = 'archive'

            if program.datetime_type == 'weekly':
                try:
                    program.timestamp_earliest = min(program.timestamps_start_weekly)
                except Exception as e:
                    logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
                    set_outdated_program()
            elif program.datetime_type == 'occasional':
                try:
                    program.timestamp_earliest = min(program.timestamps_start_occasional)
                except Exception as e:
                    logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
                    set_outdated_program()
            else:
                try:
                    timestamps_weekly_earliest = min(program.timestamps_start_weekly)
                    timestamps_occasional_earliest = min(program.timestamps_start_occasional)
                    program.timestamp_earliest = min(timestamps_weekly_earliest, timestamps_occasional_earliest)
                except Exception as e:
                    logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
                    if not program.timestamps_start_weekly and not program.timestamps_start_occasional:
                        set_outdated_program()
                    else:
                        if not program.timestamps_start_weekly:
                            program.timestamp_earliest = min(program.timestamps_start_occasional)
                        else:
                            program.timestamp_earliest = min(program.timestamps_start_weekly)
            # End Set_Timestamp_Earliest
            program.save()
        return HttpResponse('Timestamp of Programs checked.')

    except Exception as e:
        logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
        return HttpResponseServerError('Internal Server Error')


class MenuApi(views.APIView):
    def get(self, request):
        queryset = models.Menu.objects.all().order_by('num_order')
        serializer_data = serializers.MenuSerializer(queryset, many=True)
        serializer = {'menuItems': serializer_data.data}
        return response.Response(serializer, status=status.HTTP_200_OK)


# menu.json will be created automatically.
def create_menu_json(request):
    try:
        # Start Create menu.json
        file = open("static/menu.json", "w+", encoding="utf-8")  # TODO Path
        json_var = urlopen(request.build_absolute_uri(reverse('api:menu')), timeout=5).read().decode("utf-8")
        try:
            file.write(json_var)
        except Exception as e:
            logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
        finally:
            file.close()
        # End Create programs.json

        return HttpResponse('menu.json is Created.')

    except Exception as e:
        logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
        return HttpResponseServerError('Internal Server Error')


def every_10_second(request):
    # TODO Urls
    check_on_planning_status_code = requests.get('http://127.0.0.1:8000' + reverse('api:check_on_planning'),
                                                 timeout=5).status_code
    check_live_status_code = requests.get('http://127.0.0.1:8000' + reverse('api:check_live'), timeout=5).status_code
    create_programs_json_status_code = requests.get('http://127.0.0.1:8000' + reverse('api:create_programs_json'),
                                                    timeout=5).status_code
    if check_on_planning_status_code != 200 or check_live_status_code != 200 or create_programs_json_status_code != 200:
        return HttpResponseServerError('Internal Server Error')
    return HttpResponse('Everything was done successfully.')
