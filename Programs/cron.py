import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from Programs import models


def create_programs_json():
    queryset = models.Program.objects.all().filter(status='publish')

    # Specify started and unstarted programs
    for program in queryset:
        # Start Check Time of Stream
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

        # End Check Time of Stream

        # Start Check Shoutcast Stream Status
        def check_shoutcast_stream_status(stats_url):
            url_var = urlopen(stats_url)
            # We're at the root node (<main tag>)
            root_node = ET.parse(url_var).getroot()
            # Find interested in tag
            shoutcast_status = root_node.find('STREAMSTATUS').text
            return shoutcast_status

        # End Check Shoutcast Stream Status

        # Start Check Wowza Stream Status
        def check_wowza_stream_status(stats_url):
            url_var = urlopen(stats_url)
            # We're at the root node (<main tag>)
            root_node = ET.parse(url_var).getroot()
            # We need to go one level below to get (interested in tag)
            i = 1
            for tag in root_node.findall('ConnectionCount/entry/long'):
                # Get the value of the heading attribute
                if i == 3:
                    wowza_status = tag.text
                    return wowza_status
                i += 1

        # End Check Wowza Stream Status

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
                program.timestamp_earliest = []

        # End Set_Timestamps

        # Start work on error_count.txt
        def read_error_count():
            try:
                temp_var = open("error_count.txt", "r")  # TODO path
            except:
                # if file does not exist
                temp_var = open("error_count.txt", "w")  # TODO path
                temp_var.write('0')
                temp_var.close()
                temp_var = open("error_count.txt", "r")  # TODO path
            return int(temp_var.read())

        def write_error_count(num):
            temp_var = open("error_count.txt", "w")  # TODO path
            temp_var.write(num)
            temp_var.close()

        # End work on error_count.txt

        set_timestamp_earliest()
        if not check_stream_time():
            if program.is_voice_active:
                program.is_voice_active = False
            if program.is_video_active:
                program.is_video_active = False
            if program.isLive:
                program.isLive = False
                write_error_count('0')
        else:
            if program.voice_stats_type == 'shoutcast':
                if check_shoutcast_stream_status(program.voice_stats_link) == '1':
                    program.is_voice_active = True
                else:
                    program.is_voice_active = False
            elif program.voice_stats_type == 'wowza':
                if check_wowza_stream_status(program.voice_stats_link) == '1':
                    program.is_voice_active = True
                else:
                    program.is_voice_active = False
            if program.video_stats_type == 'wowza':
                if check_wowza_stream_status(program.video_stats_link) == '1':
                    program.is_video_active = True
                else:
                    program.is_video_active = False

            if program.is_voice_active is True or program.is_video_active is True:
                if not program.isLive:
                    program.isLive = True
                write_error_count('0')
            else:
                if program.isLive:
                    file = read_error_count()
                    if file == 3:
                        program.isLive = False
                        write_error_count('0')
                    else:
                        file += 1
                        write_error_count(str(file))
                        break
        program.save()

    # Start Create programs.json
    file = open("programs.json", "w+", encoding="utf-8")  # TODO path
    url_var = urlopen("http://127.0.0.1:8000/api/v1/programs/").read().decode("utf-8")  # TODO url
    file.write(url_var)
    file.close()
    # End Create programs.json
