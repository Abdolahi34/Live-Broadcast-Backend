from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django_better_admin_arrayfield.models.fields import ArrayField


class Program(models.Model):
    class Meta:
        verbose_name = 'برنامه'
        verbose_name_plural = 'برنامه ها'

    datetime_type_choices = (
        ('regular', 'منظم'),
        ('occasional', 'مناسبتی'),
    )

    regularly_choices = (
        ('daily', 'روزانه'),
        ('weekly', 'هفتگی'),
    )

    stream_type_choices = (
        ('audio', 'صوتی'),
        ('video', 'تصویری'),
        ('audio_video', 'صوتی و تصویری'),
    )

    stats_type_choices = (
        ('shoutcast', 'Shoutcast'),
        ('wowza', 'Wowza'),
    )

    title = models.CharField(max_length=50, help_text='تعداد کاراکتر مجاز 50 عدد می باشد.', verbose_name='عنوان')
    description = models.TextField(max_length=250, help_text='تعداد کاراکتر مجاز 250 عدد می باشد.',
                                   verbose_name='توضیحات')
    title_in_player = models.CharField(max_length=50, help_text='تعداد کاراکتر مجاز 50 عدد می باشد.',
                                       verbose_name='عنوان در صفحه پخش زنده')
    description_in_player = models.TextField(max_length=250, help_text='تعداد کاراکتر مجاز 250 عدد می باشد.',
                                             verbose_name='توضیحات در صفحه پخش زنده')
    slug = models.SlugField(max_length=70, help_text='تعداد کاراکتر مجاز 70 عدد می باشد.', unique=True, db_index=True,
                            verbose_name='عنوان در url')
    date_display = models.CharField(max_length=30, help_text='تعداد کاراکتر مجاز 30 عدد می باشد.',
                                    verbose_name='تاریخ نمایش داده شده به کاربر')
    datetime_type = models.CharField(max_length=10, choices=datetime_type_choices, verbose_name='نوع برگزاری برنامه')
    regularly = models.CharField(max_length=6, choices=regularly_choices, blank=True, null=True,
                                 help_text='اگر برنامه به صورت منظم برگزار می شود، روزانه یا هفتگی بودن آن را مشخص کنید.',
                                 verbose_name='روزانه / هفتگی')
    day_0 = models.BooleanField(default=False, verbose_name='شنبه ها')
    day_1 = models.BooleanField(default=False, verbose_name='یکشنبه ها')
    day_2 = models.BooleanField(default=False, verbose_name='دوشنبه ها')
    day_3 = models.BooleanField(default=False, verbose_name='سه شنبه ها')
    day_4 = models.BooleanField(default=False, verbose_name='چهارشنبه ها')
    day_5 = models.BooleanField(default=False, verbose_name='پنج شنبه ها')
    day_6 = models.BooleanField(default=False, verbose_name='جمعه ها')
    specified_date = ArrayField(models.DateField(null=True, blank=True),
                                size=10, blank=True, null=True,
                                help_text='اگر برنامه به صورت مناسبتی برگزار می شود تاریخ آن را وارد نمایید.',
                                verbose_name='تاریخ مشخص (مناسبتی)')
    start_time = models.TimeField(verbose_name='زمان شروع برنامه')
    end_time = models.TimeField(verbose_name='زمان پایان برنامه')
    logo = models.ImageField(upload_to='Programs/logo/', default='Programs/logo/default_logo.png',
                             help_text='اندازه لوگو باید 150x150 باشد.', verbose_name='لوگو')
    logo_onclick_link = models.URLField(default='https://lesansedgh.ir',
                                        help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                        verbose_name='لینک کلیک روی لوگو')
    player_background = models.ImageField(upload_to='Programs/player_background/',
                                          default='Programs/logo/default_player_background.png',
                                          help_text='اندازه تصویر پس زمینه پخش زنده باید 1000*562 باشد.',
                                          verbose_name='تصویر پس زمینه پخش زنده')
    stream_type = models.CharField(max_length=15, choices=stream_type_choices, verbose_name='نوع پخش زنده')
    voice_link = models.URLField(blank=True, null=True, help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                 verbose_name='لینک پخش زنده صوتی')
    voice_stats_link = models.URLField(blank=True, null=True, help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                       verbose_name='لینک آمار پخش زنده صوتی')
    voice_stats_type = models.CharField(blank=True, null=True, max_length=20, choices=stats_type_choices,
                                        verbose_name='نوع پلتفرم آمار پخش زنده صوتی')
    video_link = models.URLField(blank=True, null=True, help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                 verbose_name='لینک پخش زنده تصویری')
    video_stats_link = models.URLField(blank=True, null=True, help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                       verbose_name='لینک آمار پخش زنده تصویری')
    video_stats_type = models.CharField(blank=True, null=True, max_length=20, choices=stats_type_choices,
                                        verbose_name='نوع پلتفرم آمار پخش زنده تصویری')
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False, verbose_name='سازنده',
                                related_name='created_by')
    latest_modifier = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False,
                                        verbose_name='آخرین تغییر دهنده', related_name='last_modified_by')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییر')
    is_voice_active = models.BooleanField(default=False, editable=False)
    is_video_active = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.title

    def clean(self):
        if self.logo.width != 150 or self.logo.height != 150:
            raise ValidationError(
                {'logo': 'اندازه لوگو باید 150x150 باشد.'}
            )
        if self.player_background.width != 1000 or self.player_background.height != 562:
            raise ValidationError(
                {'player_background': 'اندازه تصویر پس زمینه پخش زنده باید 562x1000 باشد.'}
            )

        if self.datetime_type == 'regular':
            if self.specified_date is None:
                if self.regularly is 'weekly':
                    if self.day_0 is False and self.day_1 is False and self.day_2 is False and self.day_3 is False and self.day_4 is False and self.day_5 is False and self.day_6 is False:
                        raise ValidationError(
                            {'regularly': 'با توجه به اینکه برنامه هفتگی است، حداقل یک روز هفته را انتخاب نمایید.'}
                        )
            else:
                raise ValidationError(
                    {'specified_date': 'تاریخ در برنامه های منظم نباید وارد شود.'}
                )
        else:
            if self.regularly is not None:
                raise ValidationError(
                    {'regularly': 'با توجه به اینکه برنامه مناسبتی است، نباید روزانه یا هفتگی بودن را مشخص نمایید.'}
                )
            if self.day_0:
                raise ValidationError(
                    {'day_0': 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'}
                )
            if self.day_1:
                raise ValidationError(
                    {'day_1': 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'}
                )
            if self.day_2:
                raise ValidationError(
                    {'day_2': 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'}
                )
            if self.day_3:
                raise ValidationError(
                    {'day_3': 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'}
                )
            if self.day_4:
                raise ValidationError(
                    {'day_4': 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'}
                )
            if self.day_5:
                raise ValidationError(
                    {'day_5': 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'}
                )
            if self.day_6:
                raise ValidationError(
                    {'day_6': 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'}
                )
        if self.stream_type == 'audio':
            if self.video_link is not None:
                raise ValidationError(
                    {'video_link': 'این مقدار نمی تواند خالی باشد.'}
                )
            if self.video_stats_link is not None:
                raise ValidationError(
                    {'video_stats_link': 'این مقدار نمی تواند خالی باشد.'}
                )
            if self.video_stats_type is not None:
                raise ValidationError(
                    {'video_stats_type': 'این مقدار نمی تواند خالی باشد.'}
                )
        elif self.stream_type == 'video':
            if self.voice_link is not None:
                raise ValidationError(
                    {'voice_link': 'این مقدار نمی تواند خالی باشد.'}
                )
            if self.voice_stats_link is not None:
                raise ValidationError(
                    {'voice_stats_link': 'این مقدار نمی تواند خالی باشد.'}
                )
            if self.voice_stats_type is not None:
                raise ValidationError(
                    {'voice_stats_type': 'این مقدار نمی تواند خالی باشد.'}
                )
        else:
            if self.voice_link is None:
                raise ValidationError(
                    {'voice_link': 'این مقدار نمی تواند خالی باشد.'}
                )
            if self.voice_stats_link is None:
                raise ValidationError(
                    {'voice_stats_link': 'این مقدار نمی تواند خالی باشد.'}
                )
            if self.voice_stats_type is None:
                raise ValidationError(
                    {'voice_stats_type': 'این مقدار نمی تواند خالی باشد.'}
                )
            if self.video_link is None:
                raise ValidationError(
                    {'video_link': 'این مقدار نمی تواند خالی باشد.'}
                )
            if self.video_stats_link is None:
                raise ValidationError(
                    {'video_stats_link': 'این مقدار نمی تواند خالی باشد.'}
                )
            if self.video_stats_type is None:
                raise ValidationError(
                    {'video_stats_type': 'این مقدار نمی تواند خالی باشد.'}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Program, self).save(*args, **kwargs)


class Menu(models.Model):
    class Meta:
        verbose_name = 'منو'
        verbose_name_plural = 'منو ها'

    title = models.CharField(max_length=20, verbose_name='عنوان')
    page_url = models.URLField(verbose_name='آدرس صفحه')
    num_order = models.PositiveSmallIntegerField(verbose_name='ترتیب')

    def __str__(self):
        return self.title
