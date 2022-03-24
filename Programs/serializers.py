from rest_framework import serializers

from Programs import models


class DateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DateType
        fields = ['day_type', 'day', 'specified_date']


class VoiceStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoiceStat
        fields = ['voice_stat_link', 'voice_stat_type']


class VoiceContentSerializer(serializers.ModelSerializer):
    voice_stat = VoiceStatSerializer()

    class Meta:
        model = models.VoiceContent
        fields = ['voice_link', 'voice_stat']


class VideoStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VideoStat
        fields = ['video_stat_link', 'video_stat_type']


class VideoContentSerializer(serializers.ModelSerializer):
    video_stat = VideoStatSerializer()

    class Meta:
        model = models.VideoContent
        fields = ['video_link', 'video_stat']


class StreamTypeSerializer(serializers.ModelSerializer):
    voice_content = VoiceContentSerializer()
    video_content = VideoContentSerializer()

    class Meta:
        model = models.StreamType
        fields = ['stream_type', 'voice_content', 'video_content']


class ProgramSerializer(serializers.ModelSerializer):
    datetype = DateTypeSerializer()
    logo = serializers.SerializerMethodField()
    stream = StreamTypeSerializer()

    class Meta:
        model = models.Program
        fields = ['title', 'slug', 'datetype', 'start_time', 'end_time', 'logo_onclick_link', 'logo', 'stream']

    def get_logo(self, queryset):
        request = self.context.get('request')
        logo = queryset.logo.url
        return request.build_absolute_uri(logo)
