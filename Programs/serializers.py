from rest_framework import serializers

from Programs import models


class DateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DateType
        fields = ['day_type', 'day', 'specified_date']


class VoiceStatSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = models.VoiceStat
        fields = ['url', 'type']

    def get_url(self, obj):
        return obj.voice_stat_link

    def get_type(self, obj):
        return obj.voice_stat_type


class VoiceContentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    stats = VoiceStatSerializer(source='voice_stat')

    class Meta:
        model = models.VoiceContent
        fields = ['url', 'stats']

    def get_url(self, obj):
        return obj.voice_link


class VideoStatSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = models.VideoStat
        fields = ['url', 'type']

    def get_url(self, obj):
        return obj.video_stat_link

    def get_type(self, obj):
        return obj.video_stat_type


class VideoContentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    stats = VideoStatSerializer(source='video_stat')

    class Meta:
        model = models.VideoContent
        fields = ['url', 'stats']

    def get_url(self, obj):
        return obj.video_link


class StreamTypeSerializer(serializers.ModelSerializer):
    audio = VoiceContentSerializer(source='voice_content')
    video = VideoContentSerializer(source='video_content')

    class Meta:
        model = models.StreamType
        fields = ['audio', 'video']


class ProgramSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()
    days = serializers.SerializerMethodField()
    hours = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    streams = StreamTypeSerializer()

    class Meta:
        model = models.Program
        fields = ['title', 'key', 'days', 'hours', 'link', 'logo', 'streams']

    def get_logo(self, queryset):
        request = self.context.get('request')
        logo = queryset.logo.url
        return request.build_absolute_uri(logo)

    def get_days(self, obj):
        day = obj.datetype.day
        if day == 'shanbe':
            return 'شنبه ها'
        elif day == 'shanbe_1':
            return 'یکشنبه ها'
        elif day == 'shanbe_2':
            return 'دوشنبه ها'
        elif day == 'shanbe_3':
            return 'سه شنبه ها'
        elif day == 'shanbe_4':
            return 'چهارشنبه ها'
        elif day == 'shanbe_5':
            return 'پنج شنبه ها'
        elif day == 'jome':
            return 'جمعه ها'
        else:
            return obj.datetype.specified_date

    def get_hours(self, obj):
        return f"{obj.start_time} - {obj.end_time}"

    def get_key(self, obj):
        return obj.slug

    def get_link(self, obj):
        return obj.logo_onclick_link
