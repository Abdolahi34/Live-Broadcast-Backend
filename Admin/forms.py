from django import forms

from Programs import models


class AdminProgramForm(forms.ModelForm):
    class Meta:
        model = models.Program
        fields = '__all__'


class AdminDateTypeForm(forms.ModelForm):
    class Meta:
        model = models.DateType
        fields = '__all__'


class AdminStreamTypeForm(forms.ModelForm):
    class Meta:
        model = models.StreamType
        fields = '__all__'


class AdminVideoContentForm(forms.ModelForm):
    class Meta:
        model = models.VideoContent
        fields = '__all__'


class AdminVideoStatForm(forms.ModelForm):
    class Meta:
        model = models.VideoStat
        fields = '__all__'


class AdminVoiceContentForm(forms.ModelForm):
    class Meta:
        model = models.VoiceContent
        fields = '__all__'


class AdminVoiceStatForm(forms.ModelForm):
    class Meta:
        model = models.VoiceStat
        fields = '__all__'
