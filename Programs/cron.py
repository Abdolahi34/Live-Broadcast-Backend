import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from Programs import models


def program_isLive_check():
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

        # End Check_Stats_Status

        # Start Check_Time_of_Stream
        def check_stream_time():
            try:
                """
                در تقویم میلادی منظور از کد 0 دوشنبه می باشد.
                در تقویم شمسی منظور از کد 0 شنبه می باشد.
                """
                if program.regularly == 'weekly':
                    now_weekday = datetime.datetime.now().weekday()
                    if now_weekday == 5:  # shanbe
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_6:
                            if program.end_time_day_6 < program.start_time_day_6:
                                if datetime.datetime.now().time() <= program.end_time_day_6:
                                    return True
                        # barname emrooz
                        if program.day_0:
                            if program.start_time_day_0 < program.end_time_day_0:
                                if program.start_time_day_0 <= datetime.datetime.now().time() <= program.end_time_day_0:
                                    return True
                            else:
                                if program.start_time_day_0 <= datetime.datetime.now().time():
                                    return True
                    elif now_weekday == 6:  # 1shanbe
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_0:
                            if program.end_time_day_0 < program.start_time_day_0:
                                if datetime.datetime.now().time() <= program.end_time_day_0:
                                    return True
                        # barname emrooz
                        if program.day_1:
                            if program.start_time_day_1 < program.end_time_day_1:
                                if program.start_time_day_1 <= datetime.datetime.now().time() <= program.end_time_day_1:
                                    return True
                            else:
                                if program.start_time_day_1 <= datetime.datetime.now().time():
                                    return True
                    elif now_weekday == 0:  # 2shanbe
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_1:
                            if program.end_time_day_1 < program.start_time_day_1:
                                if datetime.datetime.now().time() <= program.end_time_day_1:
                                    return True
                        # barname emrooz
                        if program.day_2:
                            if program.start_time_day_2 < program.end_time_day_2:
                                if program.start_time_day_2 <= datetime.datetime.now().time() <= program.end_time_day_2:
                                    return True
                            else:
                                if program.start_time_day_2 <= datetime.datetime.now().time():
                                    return True
                    elif now_weekday == 1:  # 3shanbe
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_2:
                            if program.end_time_day_2 < program.start_time_day_2:
                                if datetime.datetime.now().time() <= program.end_time_day_2:
                                    return True
                        # barname emrooz
                        if program.day_3:
                            if program.start_time_day_3 < program.end_time_day_3:
                                if program.start_time_day_3 <= datetime.datetime.now().time() <= program.end_time_day_3:
                                    return True
                            else:
                                if program.start_time_day_3 <= datetime.datetime.now().time():
                                    return True
                    elif now_weekday == 2:  # 4shanbe
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_3:
                            if program.end_time_day_3 < program.start_time_day_3:
                                if datetime.datetime.now().time() <= program.end_time_day_3:
                                    return True
                        # barname emrooz
                        if program.day_4:
                            if program.start_time_day_4 < program.end_time_day_4:
                                if program.start_time_day_4 <= datetime.datetime.now().time() <= program.end_time_day_4:
                                    return True
                            else:
                                if program.start_time_day_4 <= datetime.datetime.now().time():
                                    return True
                    elif now_weekday == 3:  # 5shanbe
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_4:
                            if program.end_time_day_4 < program.start_time_day_4:
                                if datetime.datetime.now().time() <= program.end_time_day_4:
                                    return True
                        # barname emrooz
                        if program.day_5:
                            if program.start_time_day_5 < program.end_time_day_5:
                                if program.start_time_day_5 <= datetime.datetime.now().time() <= program.end_time_day_5:
                                    return True
                            else:
                                if program.start_time_day_5 <= datetime.datetime.now().time():
                                    return True
                    else:  # jome
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_5:
                            if program.end_time_day_5 < program.start_time_day_5:
                                if datetime.datetime.now().time() <= program.end_time_day_5:
                                    return True
                        # barname emrooz
                        if program.day_6:
                            if program.start_time_day_6 < program.end_time_day_6:
                                if program.start_time_day_6 <= datetime.datetime.now().time() <= program.end_time_day_6:
                                    return True
                            else:
                                if program.start_time_day_6 <= datetime.datetime.now().time():
                                    return True
                    return False
                elif program.datetime_type == 'occasional':
                    i = 0
                    while i != -1:
                        try:
                            specified_date = program.specified_date[i]
                            specified_start_time = program.specified_start_time[i]
                            specified_end_time = program.specified_end_time[i]
                        except IndexError:
                            break
                        if specified_end_time < specified_start_time:
                            # ghable 24:00:00
                            if datetime.datetime.now().date() == specified_date:
                                if specified_start_time <= datetime.datetime.now().time():
                                    return True
                            # bade 24:00:00
                            specified_date += datetime.timedelta(days=1)
                            if datetime.datetime.now().date() == specified_date:
                                if datetime.datetime.now().time() <= specified_end_time:
                                    return True
                        else:
                            if datetime.datetime.now().date() == specified_date:
                                if specified_start_time <= datetime.datetime.now().time() <= specified_end_time:
                                    return True
                        i += 1
                    return False
                else:
                    # check kardane haftegi
                    now_weekday = datetime.datetime.now().weekday()
                    if now_weekday == 5:  # shanbe
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_6:
                            if program.end_time_day_6 < program.start_time_day_6:
                                if datetime.datetime.now().time() <= program.end_time_day_6:
                                    return True
                        # barname emrooz
                        if program.day_0:
                            if program.start_time_day_0 < program.end_time_day_0:
                                if program.start_time_day_0 <= datetime.datetime.now().time() <= program.end_time_day_0:
                                    return True
                            else:
                                if program.start_time_day_0 <= datetime.datetime.now().time():
                                    return True
                    elif now_weekday == 6:  # 1shanbe
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_0:
                            if program.end_time_day_0 < program.start_time_day_0:
                                if datetime.datetime.now().time() <= program.end_time_day_0:
                                    return True
                        # barname emrooz
                        if program.day_1:
                            if program.start_time_day_1 < program.end_time_day_1:
                                if program.start_time_day_1 <= datetime.datetime.now().time() <= program.end_time_day_1:
                                    return True
                            else:
                                if program.start_time_day_1 <= datetime.datetime.now().time():
                                    return True
                    elif now_weekday == 0:  # 2shanbe
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_1:
                            if program.end_time_day_1 < program.start_time_day_1:
                                if datetime.datetime.now().time() <= program.end_time_day_1:
                                    return True
                        # barname emrooz
                        if program.day_2:
                            if program.start_time_day_2 < program.end_time_day_2:
                                if program.start_time_day_2 <= datetime.datetime.now().time() <= program.end_time_day_2:
                                    return True
                            else:
                                if program.start_time_day_2 <= datetime.datetime.now().time():
                                    return True
                    elif now_weekday == 1:  # 3shanbe
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_2:
                            if program.end_time_day_2 < program.start_time_day_2:
                                if datetime.datetime.now().time() <= program.end_time_day_2:
                                    return True
                        # barname emrooz
                        if program.day_3:
                            if program.start_time_day_3 < program.end_time_day_3:
                                if program.start_time_day_3 <= datetime.datetime.now().time() <= program.end_time_day_3:
                                    return True
                            else:
                                if program.start_time_day_3 <= datetime.datetime.now().time():
                                    return True
                    elif now_weekday == 2:  # 4shanbe
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_3:
                            if program.end_time_day_3 < program.start_time_day_3:
                                if datetime.datetime.now().time() <= program.end_time_day_3:
                                    return True
                        # barname emrooz
                        if program.day_4:
                            if program.start_time_day_4 < program.end_time_day_4:
                                if program.start_time_day_4 <= datetime.datetime.now().time() <= program.end_time_day_4:
                                    return True
                            else:
                                if program.start_time_day_4 <= datetime.datetime.now().time():
                                    return True
                    elif now_weekday == 3:  # 5shanbe
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_4:
                            if program.end_time_day_4 < program.start_time_day_4:
                                if datetime.datetime.now().time() <= program.end_time_day_4:
                                    return True
                        # barname emrooz
                        if program.day_5:
                            if program.start_time_day_5 < program.end_time_day_5:
                                if program.start_time_day_5 <= datetime.datetime.now().time() <= program.end_time_day_5:
                                    return True
                            else:
                                if program.start_time_day_5 <= datetime.datetime.now().time():
                                    return True
                    else:  # jome
                        # barname rooze ghabl ke ta bade 24:00:00 tool mikeshe
                        if program.day_5:
                            if program.end_time_day_5 < program.start_time_day_5:
                                if datetime.datetime.now().time() <= program.end_time_day_5:
                                    return True
                        # barname emrooz
                        if program.day_6:
                            if program.start_time_day_6 < program.end_time_day_6:
                                if program.start_time_day_6 <= datetime.datetime.now().time() <= program.end_time_day_6:
                                    return True
                            else:
                                if program.start_time_day_6 <= datetime.datetime.now().time():
                                    return True
                    # check kardane monasebati
                    i = 0
                    while i != -1:
                        try:
                            specified_date = program.specified_date[i]
                            specified_start_time = program.specified_start_time[i]
                            specified_end_time = program.specified_end_time[i]
                        except IndexError:
                            break
                        if specified_end_time < specified_start_time:
                            # ghable 24:00:00
                            if datetime.datetime.now().date() == specified_date:
                                if specified_start_time <= datetime.datetime.now().time():
                                    return True
                            # bade 24:00:00
                            specified_date += datetime.timedelta(days=1)
                            if datetime.datetime.now().date() == specified_date:
                                if datetime.datetime.now().time() <= specified_end_time:
                                    return True
                        else:
                            if datetime.datetime.now().date() == specified_date:
                                if specified_start_time <= datetime.datetime.now().time() <= specified_end_time:
                                    return True
                        i += 1
                    return False
            except:
                return False

        # End Check_Time_of_Stream

        check_stats_status()
        stream_time_status = check_stream_time()
        if not stream_time_status:
            if program.is_voice_active:
                queryset.filter(pk=program.pk).update(is_voice_active=False)
            if program.is_video_active:
                queryset.filter(pk=program.pk).update(is_video_active=False)
            if program.isLive:
                queryset.filter(pk=program.pk).update(isLive=False)
            if program.error_count != 0:
                queryset.filter(pk=program.pk).update(error_count=0)
        else:
            if program.is_voice_active or program.is_video_active:
                queryset.filter(pk=program.pk).update(isLive=True)
            elif program.isLive:
                if program.error_count == 6:
                    queryset.filter(pk=program.pk).update(isLive=False)
                    queryset.filter(pk=program.pk).update(error_count=0)
                else:
                    program.error_count += 1
                    queryset.filter(pk=program.pk).update(error_count=program.error_count)
