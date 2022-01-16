from django.db import models
from django.contrib.auth.models import User


class Program(models.Model):
    class StreamChoices(models.TextChoices):
        video = 'vid'
        audio = 'aud'
        video_audio = 'v_a'

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
    day = models.CharField(max_length=8, choices=DayChoices.choices, null=True)
    date = models.DateField(null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    logo_link = models.URLField()
    logo = models.ImageField(upload_to='images', default='')
    stream = models.CharField(max_length=3, choices=StreamChoices.choices, default=StreamChoices.video)
    video_link = models.URLField(blank=True, default='')
    stat_video_link = models.URLField(blank=True, default='')
    stat_video_type = models.CharField(max_length=20, choices=StatType.choices, blank=True)
    voice_link = models.URLField(blank=True, default='')
    stat_voice_link = models.URLField(blank=True, default='')
    stat_voice_type = models.CharField(max_length=20, choices=StatType.choices, blank=True)
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title
