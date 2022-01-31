from django import forms
from Programs import models
# from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
# from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
# from django.utils.translation import gettext_lazy as _


# class AddDateTypeForm(forms.ModelForm):
#     class Meta:
#         model = models.DateType
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super(AddDateTypeForm, self).__init__(*args, **kwargs)
#         self.fields['specified_date'] = JalaliDateField(widget=AdminJalaliDateWidget
# optional, to use default datepicker
#                                                         )
# you can added a "class" to this field for use your datepicker!
# self.fields['specified_date'].widget.attrs.update({'class': 'jalali_date-date'})
#
# self.fields['specified_date'] = SplitJalaliDateTimeField(widget=AdminSplitJalaliDateTime
#                                                         # required, for decompress DatetimeField to JalaliDateField and JalaliTimeField
# )

# def save(self, *args, **kwargs):
#     super(AddDateTypeForm, self).save(*args, **kwargs)


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
