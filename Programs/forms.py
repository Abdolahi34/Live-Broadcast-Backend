from django import forms
from Programs import models


class AddProgramForm(forms.ModelForm):
    class Meta:
        model = models.Program
        exclude = ['created_by', 'last_modified_by', 'is_active', 'date_created', 'date_modified']


class AddStreamTypeForm(forms.ModelForm):
    class Meta:
        model = models.StreamType
        fields = ['stream_type']


class AddVideoContentForm(forms.ModelForm):
    class Meta:
        model = models.VideoContent
        fields = ['video_link']


class AddVideoStatForm(forms.ModelForm):
    class Meta:
        model = models.VideoStat
        fields = '__all__'


class AddVoiceContentForm(forms.ModelForm):
    class Meta:
        model = models.VoiceContent
        fields = ['voice_link']


class AddVoiceStatForm(forms.ModelForm):
    class Meta:
        model = models.VoiceStat
        fields = '__all__'


class AddDateTypeForm(forms.ModelForm):
    class Meta:
        model = models.DateType
        fields = '__all__'
