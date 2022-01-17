from rest_framework import serializers
from Programs.models import Program


class ProgramSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Program
        fields = [
            'title',
            'slug',
            'day',
            'date',
            'start_time',
            'end_time',
            'logo_link',
            'logo',
            'stream',
            'video_link',
            'stat_video_link',
            'stat_video_type',
            'voice_link',
            'stat_voice_link',
            'stat_voice_type',
        ]

