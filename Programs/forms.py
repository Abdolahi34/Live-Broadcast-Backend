from django import forms
from . import models


class AddProgramForm(forms.ModelForm):
    class Meta:
        model = models.Program
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

