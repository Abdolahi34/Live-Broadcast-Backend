from rest_framework import serializers

from Programs import models


class DateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DateType
        fields = '__all__'


class VoiceStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoiceStat
        fields = '__all__'


class VoiceContentSerializer(serializers.ModelSerializer):
    voice_stat = VoiceStatSerializer()

    class Meta:
        model = models.VoiceContent
        fields = ['voice_link', 'voice_stat']


class VideoStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VideoStat
        fields = '__all__'


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
    date_type = DateTypeSerializer()
    stream = StreamTypeSerializer()


    class Meta:
        model = models.Program
        fields = ['title', 'slug', 'date_type', 'start_time', 'end_time', 'logo_link', 'logo', 'stream']
