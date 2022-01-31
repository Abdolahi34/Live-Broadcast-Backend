from django.db import models
from django.contrib.auth import get_user_model

class DateType(models.Model):
    class DayTypeChoices(models.TextChoices):
        هفتگی = 'weekly'
        مناسبتی = 'occasional'

    class DayChoices(models.TextChoices):
        شنبه = 'shanbe'
        شبنه_1 = 'shanbe_1'
        شبنه_2 = 'shanbe_2'
        شبنه_3 = 'shanbe_3'
        شبنه_4 = 'shanbe_4'
        شبنه_5 = 'shanbe_5'
        جمعه = 'jome'

    day_type = models.CharField(max_length=10, choices=DayTypeChoices.choices, verbose_name='نوع')
    day = models.CharField(max_length=8, choices=DayChoices.choices, blank=True, null=True, verbose_name='هفتگی')
    specified_date = models.DateField(null=True, blank=True, verbose_name='مناسبتی')

    def __str__(self):
        return f'{self.day_type} & {self.day} & {self.specified_date}'


class VoiceStat(models.Model):
    class StatTypeChoices(models.TextChoices):
        shoutcast = 'shoutcast'
        wowza = 'wowza'

    voice_stat_link = models.URLField(blank=True, null=True, verbose_name='Stat Link')
    voice_stat_type = models.CharField(max_length=20, choices=StatTypeChoices.choices, blank=True, null=True,
                                       verbose_name='Stat Type')

    def __str__(self):
        if self.voice_stat_link is not None:
            temp1 = self.voice_stat_link
        else:
            temp1 = None
        if self.voice_stat_type is not None:
            temp2 = self.voice_stat_type
        else:
            temp2 = None
        return f'{temp1} & {temp2}'


class VoiceContent(models.Model):
    voice_link = models.URLField(blank=True, null=True, verbose_name='لینک پخش زنده صوتی')
    voice_stat = models.ForeignKey(VoiceStat, on_delete=models.CASCADE, verbose_name='Voice Stat')

    def __str__(self):
        if self.voice_link is not None:
            temp1 = self.voice_link
        else:
            temp1 = None
        if self.voice_stat is not None and self.voice_stat.voice_stat_link is not None:
            temp2 = self.voice_stat.voice_stat_link
        else:
            temp2 = None
        return f'{temp1} & {temp2}'


class VideoStat(models.Model):
    class StatTypeChoices(models.TextChoices):
        shoutcast = 'shoutcast'
        wowza = 'wowza'

    video_stat_link = models.URLField(blank=True, null=True, verbose_name='Stat Link')
    video_stat_type = models.CharField(max_length=20, choices=StatTypeChoices.choices, blank=True, null=True,
                                       verbose_name='Stat Type')

    def __str__(self):
        if self.video_stat_link is not None:
            temp1 = self.video_stat_link
        else:
            temp1 = None
        if self.video_stat_type is not None:
            temp2 = self.video_stat_type
        else:
            temp2 = None
        return f'{temp1} & {temp2}'


class VideoContent(models.Model):
    video_link = models.URLField(blank=True, null=True, verbose_name='لینک پخش زنده صوتی')
    video_stat = models.ForeignKey(VideoStat, on_delete=models.CASCADE, verbose_name='Video Stat')

    def __str__(self):
        if self.video_link is not None:
            temp1 = self.video_link
        else:
            temp1 = None
        if self.video_stat is not None and self.video_stat.video_stat_link is not None:
            temp2 = self.video_stat.video_stat_link
        else:
            temp2 = None
        return f'{temp1} & {temp2}'


class StreamType(models.Model):
    class StreamTypeChoices(models.TextChoices):
        صوتی = 'audio'
        تصویری = 'video'
        صوتی_و_تصویری = 'video_audio'

    stream_type = models.CharField(max_length=15, choices=StreamTypeChoices.choices,
                                   default=StreamTypeChoices.صوتی_و_تصویری, verbose_name='نوع پخش زنده')
    voice_content = models.ForeignKey(VoiceContent, on_delete=models.CASCADE, verbose_name='صوتی')
    video_content = models.ForeignKey(VideoContent, on_delete=models.CASCADE, verbose_name='تصویری')

    def __str__(self):
        if self.voice_content is not None and self.voice_content.voice_link is not None:
            temp1 = self.voice_content.voice_link
        else:
            temp1 = None
        if self.video_content is not None and self.video_content.video_link is not None:
            temp2 = self.video_content.video_link
        else:
            temp2 = None
        return f'{self.stream_type} & {temp1} & {temp2}'


class Program(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    slug = models.SlugField(max_length=70, unique=True, db_index=True, verbose_name='slug')
    date_type = models.ForeignKey(DateType, on_delete=models.CASCADE, verbose_name='تاریخ')
    start_time = models.TimeField(verbose_name='زمان شروع')
    end_time = models.TimeField(verbose_name='زمان پایان')
    logo_link = models.URLField(default='https://lesansedgh.ir', verbose_name='لینک لوگو')
    logo = models.ImageField(upload_to='Programs/images/%Y_%m_%d', default='Programs/images/default_logo.png',
                             verbose_name='عکس')
    stream = models.ForeignKey(StreamType, on_delete=models.CASCADE, verbose_name='محتویات برنامه')
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False, verbose_name='ایجاد کننده',
                                   related_name='created')
    last_modified_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False,
                                         verbose_name='آخرین تغییر دهنده', related_name='last_modified')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییر')

    def __str__(self):
        return self.title
