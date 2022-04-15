from rest_framework import serializers
import datetime

from Programs import models


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = ['title', 'href']

    href = serializers.SerializerMethodField()

    def get_href(self, obj):
        return obj.page_url


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Program
        fields = ['title', 'key', 'description', 'title1', 'title2', 'days', 'hours', 'link', 'logo',
                  'isLive', 'streams']

    key = serializers.SerializerMethodField()
    title1 = serializers.SerializerMethodField()
    title2 = serializers.SerializerMethodField()
    days = serializers.SerializerMethodField()
    hours = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    isLive = serializers.SerializerMethodField()
    streams = serializers.SerializerMethodField()

    def get_key(self, obj):
        return obj.slug

    def get_title1(self, obj):
        return obj.title_in_player

    def get_title2(self, obj):
        return obj.description_in_player

    def get_days(self, obj):
        return obj.date_display

    def get_hours(self, obj):
        return f"ساعت {obj.start_time} تا {obj.end_time}"

    def get_link(self, obj):
        return obj.logo_onclick_link

    def get_logo(self, queryset):
        request = self.context.get('request')
        logo = queryset.logo.url
        return request.build_absolute_uri(logo)

    def get_isLive(self, obj):
        if obj.isLive:
            base_datetime = datetime.datetime
            now_weekday = datetime.datetime.now().isoweekday()

            if obj.datetime_type == 'regular':
                '''
                روز اول هفته در تقویم میلادی دوشنبه در نظر گرفته شده.
                در تقویم میلادی منظور از کد 0 یکشنبه می باشد.
                در تقویم شمسی منظور از کد 0 شنبه می باشد.
                '''
                if obj.regularly == 'daily':
                    start_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                        base_datetime.now().day, obj.start_time.hour,
                                                        obj.start_time.minute, obj.start_time.second, 0)
                    end_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                      base_datetime.now().day, obj.start_time.hour,
                                                      obj.start_time.minute, obj.start_time.second, 0)
                    if end_time_datetime < base_datetime.now() < start_time_datetime:
                        obj.isLive = False
                else:
                    if obj.day_0:
                        if now_weekday == 6:
                            start_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                                base_datetime.now().day, obj.start_time.hour,
                                                                obj.start_time.minute, obj.start_time.second, 0)
                            end_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                              base_datetime.now().day, obj.start_time.hour,
                                                              obj.start_time.minute, obj.start_time.second, 0)
                            if end_time_datetime < base_datetime.now() < start_time_datetime:
                                obj.isLive = False
                    elif obj.day_1:
                        if now_weekday == 0:
                            start_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                                base_datetime.now().day, obj.start_time.hour,
                                                                obj.start_time.minute, obj.start_time.second, 0)
                            end_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                              base_datetime.now().day, obj.start_time.hour,
                                                              obj.start_time.minute, obj.start_time.second, 0)
                            if end_time_datetime < base_datetime.now() < start_time_datetime:
                                obj.isLive = False
                    elif obj.day_2:
                        if now_weekday == 1:
                            start_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                                base_datetime.now().day, obj.start_time.hour,
                                                                obj.start_time.minute, obj.start_time.second, 0)
                            end_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                              base_datetime.now().day, obj.start_time.hour,
                                                              obj.start_time.minute, obj.start_time.second, 0)
                            if end_time_datetime < base_datetime.now() < start_time_datetime:
                                obj.isLive = False
                    elif obj.day_3:
                        if now_weekday == 2:
                            start_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                                base_datetime.now().day, obj.start_time.hour,
                                                                obj.start_time.minute, obj.start_time.second, 0)
                            end_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                              base_datetime.now().day, obj.start_time.hour,
                                                              obj.start_time.minute, obj.start_time.second, 0)
                            if end_time_datetime < base_datetime.now() < start_time_datetime:
                                obj.isLive = False
                    elif obj.day_4:
                        if now_weekday == 3:
                            start_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                                base_datetime.now().day, obj.start_time.hour,
                                                                obj.start_time.minute, obj.start_time.second, 0)
                            end_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                              base_datetime.now().day, obj.start_time.hour,
                                                              obj.start_time.minute, obj.start_time.second, 0)
                            if end_time_datetime < base_datetime.now() < start_time_datetime:
                                obj.isLive = False
                    elif obj.day_5:
                        if now_weekday == 4:
                            start_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                                base_datetime.now().day, obj.start_time.hour,
                                                                obj.start_time.minute, obj.start_time.second, 0)
                            end_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                              base_datetime.now().day, obj.start_time.hour,
                                                              obj.start_time.minute, obj.start_time.second, 0)
                            if end_time_datetime < base_datetime.now() < start_time_datetime:
                                obj.isLive = False
                    else:
                        if now_weekday == 5:
                            start_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                                base_datetime.now().day, obj.start_time.hour,
                                                                obj.start_time.minute, obj.start_time.second, 0)
                            end_time_datetime = base_datetime(base_datetime.now().year, base_datetime.now().month,
                                                              base_datetime.now().day, obj.start_time.hour,
                                                              obj.start_time.minute, obj.start_time.second, 0)
                            if end_time_datetime < base_datetime.now() < start_time_datetime:
                                obj.isLive = False
            else:
                is_today = False
                for specified_date in obj.specified_date:
                    if base_datetime.now().date() == specified_date:
                        is_today = True
                        break
                if not is_today:
                    obj.isLive = False
        else:
            obj.isLive = False

        return obj.isLive

    def get_streams(self, obj):
        request = self.context.get('request')
        player_background = obj.player_background.url
        player_background_2 = request.build_absolute_uri(player_background)

        if obj.voice_stats_type == None:
            obj.voice_stats_type = ''
        if obj.video_stats_type == None:
            obj.video_stats_type = ''


        return {
            'audio': {
                'url': obj.voice_link,
                'stats': {
                    'url': obj.voice_stats_link,
                    'type': obj.voice_stats_type
                }
            },
            'video': {
                'url': obj.video_link,
                'stats': {
                    'url': obj.video_stats_link,
                    'type': obj.video_stats_type
                }
            },
            'image': {'url': player_background_2}
        }
