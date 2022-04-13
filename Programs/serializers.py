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
                  'isLive', 'streams', 'image']

    key = serializers.SerializerMethodField()
    title1 = serializers.SerializerMethodField()
    title2 = serializers.SerializerMethodField()
    days = serializers.SerializerMethodField()
    hours = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    isLive = serializers.SerializerMethodField()
    streams = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_key(self, obj):
        return obj.slug

    def get_title1(self, obj):
        return obj.title_in_player

    def get_title2(self, obj):
        return obj.description_in_player

    # TODO
    def get_days(self, obj):
        return obj.date_display
        # if obj.date_time.datetime_type == 'daily':
        #     return 'هر روز'
        # elif obj.date_time.datetime_type == 'weekly':
        #     if obj.date_time.week_day == 'shanbe':
        #         return 'شنبه ها'
        #     elif obj.date_time.week_day == 'shanbe_1':
        #         return 'یکشنبه ها'
        #     elif obj.date_time.week_day == 'shanbe_2':
        #         return 'دوشنبه ها'
        #     elif obj.date_time.week_day == 'shanbe_3':
        #         return 'سه شنبه ها'
        #     elif obj.date_time.week_day == 'shanbe_4':
        #         return 'چهارشنبه ها'
        #     elif obj.date_time.week_day == 'shanbe_5':
        #         return 'پنج شنبه ها'
        #     elif obj.date_time.week_day == 'jome':
        #         return 'جمعه ها'
        # else:
        #     return obj.date_time.specified_date

    def get_hours(self, obj):
        return f"ساعت {obj.date_time.start_time} تا {obj.date_time.end_time}"

    def get_link(self, obj):
        return obj.logo_onclick_link

    def get_logo(self, queryset):
        request = self.context.get('request')
        logo = queryset.logo.url
        return request.build_absolute_uri(logo)

    # TODO اگر الان زمانی بود که بین زمان شروع و پایان برنامه قرار داشت و پخش وصل بود علامت  قرمز پخش زنده فعال می شود
    def get_isLive(self, obj):
        if obj.date_time.datetime_type == 'daily':

            return 'هر روز'
        elif obj.date_time.datetime_type == 'weekly':
            pass
        else:
            return obj.date_time.specified_date

        program_start_time = 0
        program_end_time = 0
        if program_start_time <= datetime.datetime.now().timestamp() <= program_end_time:
            if obj.is_voice_active or obj.is_video_active:
                return 'true'
            else:
                return 'false'
        return 'false'

    def get_streams(self, obj):
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
            }
        }

    def get_image(self, queryset):
        request = self.context.get('request')
        player_background = queryset.player_background.url
        return {'url': request.build_absolute_uri(player_background)}
