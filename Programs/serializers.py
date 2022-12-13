from rest_framework import serializers

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
        if not obj.isLive:
            return 'برنامه شروع نشده است.'
        else:
            return obj.title_in_player

    def get_title2(self, obj):
        return obj.description_in_player

    def get_days(self, obj):
        return obj.date_display

    def get_hours(self, obj):
        return obj.time_display

    def get_link(self, obj):
        return obj.logo_link

    def get_logo(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.logo.url)

    def get_isLive(self, obj):
        return obj.isLive

    def get_streams(self, obj):
        streams = {}

        if obj.is_audio_active:
            request = self.context.get('request')
            player_background = request.build_absolute_uri(obj.player_background.url)
            streams['audio'] = {
                'url': obj.audio_link,
                'stats': {
                    'url': obj.audio_stats_link,
                    'type': obj.audio_platform_type
                },
                'image': {'url': player_background}
            }
        if obj.is_video_active:
            streams['video'] = {
                'url': obj.video_link,
                'stats': {
                    'url': obj.video_stats_link,
                    'type': obj.video_platform_type
                }
            }

        return streams
