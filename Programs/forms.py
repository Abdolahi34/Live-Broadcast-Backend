from django import forms
from Programs import models
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from django.utils.translation import gettext_lazy as _


class AddDateTypeForm(forms.ModelForm):
    class Meta:
        model = models.DateType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddDateTypeForm, self).__init__(*args, **kwargs)
        self.fields['specified_date'] = JalaliDateField(widget=AdminJalaliDateWidget
                                                        # optional, to use default datepicker
                                                        )
        # you can added a "class" to this field for use your datepicker!
        # self.fields['specified_date'].widget.attrs.update({'class': 'jalali_date-date'})

        # self.fields['specified_date'] = SplitJalaliDateTimeField(widget=AdminSplitJalaliDateTime
        #                                                         # required, for decompress DatetimeField to JalaliDateField and JalaliTimeField
        #                                                         )

    def save(self, *args, **kwargs):
        super(AddDateTypeForm, self).save(*args, **kwargs)


class AddProgramForm(forms.Form):
    title = forms.CharField(max_length=100)
    slug = forms.SlugField(max_length=70)

    date = AddDateTypeForm()

    start_time = forms.TimeField()
    end_time = forms.TimeField()
    logo_link = forms.URLField()
    logo = forms.ImageField()

    stream_type = forms.ChoiceField(choices=models.StreamType.StreamTypeChoices.choices)
    voice_link = forms.URLField(required=False)
    voice_stat_link = forms.URLField(required=False)
    voice_stat_type = forms.ChoiceField(choices=models.VoiceStat.StatTypeChoices.choices, required=False)
    video_link = forms.URLField(required=False)
    video_stat_link = forms.URLField(required=False)
    video_stat_type = forms.ChoiceField(choices=models.VideoStat.StatTypeChoices.choices, required=False)

    def save(self, *args, **kwargs):
        super(AddProgramForm, self).save(*args, **kwargs)