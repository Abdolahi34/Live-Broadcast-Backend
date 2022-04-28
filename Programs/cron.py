import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from Programs import models


def program_isLive_check():
    queryset = models.Program.objects.all().filter(status='publish')

    # Start Check_Stats_Status
    def check_stats_status():
        global stats_status
        try:
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
            if program.voice_stats_type == 'wowza' or program.video_stats_type == 'wowza':
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
            stats_status = True
        except:
            stats_status = False

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

        if stats_status:
            if not check_stream_time():
                if program.is_voice_active:
                    queryset.filter(pk=program.pk).update(is_voice_active=False)
                if program.is_video_active:
                    queryset.filter(pk=program.pk).update(is_video_active=False)
                if program.isLive:
                    queryset.filter(pk=program.pk).update(isLive=False)
                    queryset.filter(pk=program.pk).update(error_count=0)
            else:
                if program.is_voice_active or program.is_video_active:
                    queryset.filter(pk=program.pk).update(isLive=True)
                elif program.isLive:
                    if program.error_count == 3:
                        queryset.filter(pk=program.pk).update(isLive=False)
                        queryset.filter(pk=program.pk).update(error_count=0)
                    else:
                        program.error_count += 1
                        queryset.filter(pk=program.pk).update(error_count=program.error_count)
                else:
                    queryset.filter(pk=program.pk).update(error_count=0)
        else:
            break
