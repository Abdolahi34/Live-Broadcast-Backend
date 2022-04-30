import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from Programs import models


def program_isLive_check():
    queryset = models.Program.objects.all().filter(status='publish')

    # Start Check_Stats_Status
    def check_stats_status():
        global shoutcast_stream_status, wowza_stream_status
        # try:
        url_var = urlopen('https://radio.masjedsafa.com/stats?sid=2')
        # We're at the root node (<main tag>)
        root_node = ET.parse(url_var).getroot()
        # Find interested in tag
        shoutcast_stream_status = root_node.find('STREAMSTATUS').text

        url_var = urlopen(
            'https://live.mostadrak.org/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/masjed/monitoring/current')
        # We're at the root node (<main tag>)
        root_node = ET.parse(url_var).getroot()
        # We need to go one level below to get (interested in tag)
        i = 1
        for tag in root_node.findall('ConnectionCount/entry/long'):
            # Get the value of the heading attribute
            if i == 3:
                wowza_stream_status = tag.text
                break
            i += 1

    # End Check_Stats_Status

    # Specify started and unstarted programs
    check_stats_status()
    for program in queryset:
        # Start Check_Time_of_Stream
        def check_stream_time():
            def check_timestamp(start_timestamp, end_timestamp):
                i = 0
                while i != -1:
                    try:
                        if start_timestamp[i] <= now_timestamp:
                            if now_timestamp < end_timestamp[i]:
                                return True
                        i += 1
                    except:
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
                if check_timestamp(program.timestamps_start_weekly, program.timestamps_end_weekly) or check_timestamp(
                        program.timestamps_start_occasional, program.timestamps_end_occasional):
                    return True
                else:
                    return False

        # End Check_Time_of_Stream

        def read_error_count():
            temp_var = open("error_count.txt", "r")
            return int(temp_var.read())

        def write_error_count(num):
            temp_var = open("error_count.txt", "w")
            temp_var.write(num)
            temp_var.close()

        if not check_stream_time():
            if program.is_voice_active:
                queryset.filter(pk=program.pk).update(is_voice_active=False)
            if program.is_video_active:
                queryset.filter(pk=program.pk).update(is_video_active=False)
            if program.isLive:
                queryset.filter(pk=program.pk).update(isLive=False)
                write_error_count(0)
        else:
            if program.voice_stats_type == 'shoutcast' and shoutcast_stream_status == '1':
                queryset.filter(pk=program.pk).update(is_voice_active=True)
                program.is_voice_active = True
            elif program.voice_stats_type == 'wowza' and wowza_stream_status == '1':
                queryset.filter(pk=program.pk).update(is_voice_active=True)
                program.is_voice_active = True
            elif program.is_voice_active:
                queryset.filter(pk=program.pk).update(is_voice_active=False)
                program.is_voice_active = False
            if program.video_stats_type == 'wowza' and wowza_stream_status == '1':
                queryset.filter(pk=program.pk).update(is_video_active=True)
                program.is_video_active = True
            elif program.is_video_active:
                queryset.filter(pk=program.pk).update(is_video_active=False)
                program.is_video_active = False
            if shoutcast_stream_status == '0' and wowza_stream_status == '0':
                if program.isLive:
                    file = read_error_count()
                    if file == 3:
                        queryset.filter(pk=program.pk).update(isLive=False)
                        write_error_count(0)
                    else:
                        file += 1
                        write_error_count(file)
                else:
                    write_error_count(0)
            else:
                if not program.isLive:
                    queryset.filter(pk=program.pk).update(isLive=True)
                write_error_count(0)
