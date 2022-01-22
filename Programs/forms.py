from django import forms
from . import models


class AddProgramForm(forms.ModelForm):
    class Meta:
        model = models.Program
        fields = [
            'title',
            'slug',
            'date_type',
            'start_time',
            'end_time',
            'logo_link',
            'logo',
            'stream',
        ]


class AddStreamTypeForm(forms.ModelForm):
    class Meta:
        model = models.StreamType
        fields = '__all__'


class AddVideoContentForm(forms.ModelForm):
    class Meta:
        model = models.VideoContent
        fields = '__all__'


class AddVideoStatForm(forms.ModelForm):
    class Meta:
        model = models.VideoStat
        fields = '__all__'


class AddVoiceContentForm(forms.ModelForm):
    class Meta:
        model = models.VoiceContent
        fields = '__all__'


class AddVoiceStatForm(forms.ModelForm):
    class Meta:
        model = models.VoiceStat
        fields = '__all__'


class AddDateTypeForm(forms.ModelForm):
    class Meta:
        model = models.DateType
        fields = '__all__'
