from django.db import models
from django.contrib.auth.models import User


class Program(models.Model):
    class StreamChoices(models.TextChoices):
        صوتی = 'audio'
        تصویری = 'video'
        صوتی_و_تصویری = 'video_audio'

    class DayChoices(models.TextChoices):
        شنبه = 'shanbe'
        شبنه_1 = 'shanbe_1'
        شبنه_2 = 'shanbe_2'
        شبنه_3 = 'shanbe_3'
        شبنه_4 = 'shanbe_4'
        شبنه_5 = 'shanbe_5'
        جمعه = 'jome'

    class StatType(models.TextChoices):
        shoutcast = 'shoutcast'
        wowza = 'wowza'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=70, unique=True)
    day = models.CharField(max_length=8, choices=DayChoices.choices, blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    logo_link = models.URLField(default='https://lesansedgh.ir')
    logo = models.ImageField(upload_to='Programs/images/%Y_%m_%d', default='Programs/images/default_logo.png')
    stream = models.CharField(max_length=11, choices=StreamChoices.choices, default=StreamChoices.تصویری)
    video_link = models.URLField(blank=True, null=True, default='')
    stat_video_link = models.URLField(blank=True, default='', null=True)
    stat_video_type = models.CharField(max_length=20, choices=StatType.choices, blank=True, null=True)
    voice_link = models.URLField(blank=True, default='', null=True)
    stat_voice_link = models.URLField(blank=True, default='', null=True)
    stat_voice_type = models.CharField(max_length=20, choices=StatType.choices, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
