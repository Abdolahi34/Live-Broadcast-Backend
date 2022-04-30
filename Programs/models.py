from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django_better_admin_arrayfield.models.fields import ArrayField


class Program(models.Model):
    class Meta:
        verbose_name = 'برنامه'
        verbose_name_plural = 'برنامه ها'

    status_choices = (
        ('publish', 'انتشار'),
        ('draft', 'پیش نویس'),
        ('archive', 'آرشیو'),
    )

    datetime_type_choices = (
        ('weekly', 'هفتگی'),
        ('occasional', 'مناسبتی'),
        ('weekly_occasional', 'هفتگی_مناسبتی'),
    )

    stream_type_choices = (
        ('audio', 'صوتی'),
        ('video', 'تصویری'),
        ('audio_video', 'صوتی و تصویری'),
    )

    audio_stats_type_choices = (
        ('shoutcast', 'Shoutcast'),
        ('wowza', 'Wowza'),
    )

    video_stats_type_choices = (
        ('wowza', 'Wowza'),
    )

    status = models.CharField(max_length=7, choices=status_choices, verbose_name='وضعیت برنامه')
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
    time_display = models.CharField(max_length=30, help_text='تعداد کاراکتر مجاز 30 عدد می باشد.',
                                    verbose_name='ساعت نمایش داده شده به کاربر')
    datetime_type = models.CharField(max_length=17, choices=datetime_type_choices, verbose_name='نوع برگزاری برنامه')
    day_0 = models.BooleanField(default=False, verbose_name='شنبه ها')
    start_time_day_0 = models.TimeField(blank=True, null=True, verbose_name='ساعت شروع برنامه (شنبه ها)')
    end_time_day_0 = models.TimeField(blank=True, null=True, verbose_name='ساعت پایان برنامه (شنبه ها)')
    day_1 = models.BooleanField(default=False, verbose_name='یکشنبه ها')
    start_time_day_1 = models.TimeField(blank=True, null=True, verbose_name='ساعت شروع برنامه (یکشنبه ها)')
    end_time_day_1 = models.TimeField(blank=True, null=True, verbose_name='ساعت پایان برنامه (یکشنبه ها)')
    day_2 = models.BooleanField(default=False, verbose_name='دوشنبه ها')
    start_time_day_2 = models.TimeField(blank=True, null=True, verbose_name='ساعت شروع برنامه (دوشنبه ها)')
    end_time_day_2 = models.TimeField(blank=True, null=True, verbose_name='ساعت پایان برنامه (دوشنبه ها)')
    day_3 = models.BooleanField(default=False, verbose_name='سه شنبه ها')
    start_time_day_3 = models.TimeField(blank=True, null=True, verbose_name='ساعت شروع برنامه (سه شنبه ها)')
    end_time_day_3 = models.TimeField(blank=True, null=True, verbose_name='ساعت پایان برنامه (سه شنبه ها)')
    day_4 = models.BooleanField(default=False, verbose_name='چهارشنبه ها')
    start_time_day_4 = models.TimeField(blank=True, null=True, verbose_name='ساعت شروع برنامه (چهارشنبه ها)')
    end_time_day_4 = models.TimeField(blank=True, null=True, verbose_name='ساعت پایان برنامه (چهارشنبه ها)')
    day_5 = models.BooleanField(default=False, verbose_name='پنج شنبه ها')
    start_time_day_5 = models.TimeField(blank=True, null=True, verbose_name='ساعت شروع برنامه (پنج شنبه ها)')
    end_time_day_5 = models.TimeField(blank=True, null=True, verbose_name='ساعت پایان برنامه (پنج شنبه ها)')
    day_6 = models.BooleanField(default=False, verbose_name='جمعه ها')
    start_time_day_6 = models.TimeField(blank=True, null=True, verbose_name='ساعت شروع برنامه (جمعه ها)')
    end_time_day_6 = models.TimeField(blank=True, null=True, verbose_name='ساعت پایان برنامه (جمعه ها)')
    start_date = models.DateField(blank=True, null=True, verbose_name='تاریخ شروع برنامه هفتگی')
    end_date = models.DateField(blank=True, null=True, verbose_name='تاریخ پایان برنامه هفتگی')
    timestamps_start_weekly = ArrayField(models.PositiveBigIntegerField(blank=True, null=True), editable=False,
                                         blank=True, null=True)
    timestamps_end_weekly = ArrayField(models.PositiveBigIntegerField(blank=True, null=True), editable=False,
                                       blank=True, null=True)
    specified_date = ArrayField(models.DateField(blank=True, null=True),
                                blank=True, null=True, verbose_name='تاریخ برنامه مناسبتی',
                                help_text='اگر برنامه به صورت مناسبتی برگزار می شود تاریخ آن را وارد نمایید. (مثال: 01-01-2022)')
    specified_start_time = ArrayField(models.TimeField(blank=True, null=True),
                                      blank=True, null=True, verbose_name='ساعت شروع برنامه مناسبتی',
                                      help_text='اگر برنامه به صورت مناسبتی برگزار می شود ساعت شروع آن را وارد نمایید. (مثال: 16:00:00)')
    specified_end_time = ArrayField(models.TimeField(blank=True, null=True),
                                    blank=True, null=True, verbose_name='ساعت پایان برنامه مناسبتی',
                                    help_text='اگر برنامه به صورت مناسبتی برگزار می شود ساعت پایان آن را وارد نمایید. (مثال: 16:00:00)')
    timestamps_start_occasional = ArrayField(models.PositiveBigIntegerField(blank=True, null=True), editable=False,
                                             blank=True, null=True)
    timestamps_end_occasional = ArrayField(models.PositiveBigIntegerField(blank=True, null=True), editable=False,
                                           blank=True, null=True)
    timestamp_earliest = models.PositiveBigIntegerField(blank=True, null=True, editable=False)
    logo = models.ImageField(upload_to='Programs/logo/', help_text='نسبت طول و عرض لوگو باید 1:1 باشد.',
                             verbose_name='لوگو')
    logo_link = models.URLField(default='https://lesansedgh.ir',
                                help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                verbose_name='لینک لوگو')
    player_background = models.ImageField(upload_to='Programs/player_background/', blank=True, null=True,
                                          help_text='نسبت طول و عرض تصویر پس زمینه پخش زنده باید 16:9 باشد.',
                                          verbose_name='تصویر پس زمینه پخش زنده')
    stream_type = models.CharField(max_length=11, choices=stream_type_choices, verbose_name='نوع پخش زنده')
    voice_link = models.URLField(blank=True, null=True, help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                 verbose_name='لینک پخش زنده صوتی')
    voice_stats_link = models.URLField(blank=True, null=True, help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                       verbose_name='لینک آمار پخش زنده صوتی')
    voice_stats_type = models.CharField(blank=True, null=True, max_length=9, choices=audio_stats_type_choices,
                                        verbose_name='نوع پلتفرم آمار پخش زنده صوتی')
    video_link = models.URLField(blank=True, null=True, help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                 verbose_name='لینک پخش زنده تصویری')
    video_stats_link = models.URLField(blank=True, null=True, help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                       verbose_name='لینک آمار پخش زنده تصویری')
    video_stats_type = models.CharField(blank=True, null=True, max_length=9, choices=video_stats_type_choices,
                                        verbose_name='نوع پلتفرم آمار پخش زنده تصویری')
    is_voice_active = models.BooleanField(default=False, editable=False)
    is_video_active = models.BooleanField(default=False, editable=False)
    isLive = models.BooleanField(default=False, editable=False)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False, verbose_name='سازنده',
                                related_name='created_by_program')
    latest_modifier = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False,
                                        verbose_name='آخرین تغییر دهنده', related_name='last_modified_by_program')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییر')

    def __str__(self):
        return self.title

    def clean(self):
        errors = {}

        def validate_weekly():
            if self.day_0:
                if self.start_time_day_0 is None:
                    errors['start_time_day_0'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_0 is None:
                    errors['end_time_day_0'] = 'این مقدار نمی تواند خالی باشد.'
            if self.day_1:
                if self.start_time_day_1 is None:
                    errors['start_time_day_1'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_1 is None:
                    errors['end_time_day_1'] = 'این مقدار نمی تواند خالی باشد.'
            if self.day_2:
                if self.start_time_day_2 is None:
                    errors['start_time_day_2'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_2 is None:
                    errors['end_time_day_2'] = 'این مقدار نمی تواند خالی باشد.'
            if self.day_3:
                if self.start_time_day_3 is None:
                    errors['start_time_day_3'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_3 is None:
                    errors['end_time_day_3'] = 'این مقدار نمی تواند خالی باشد.'
            if self.day_4:
                if self.start_time_day_4 is None:
                    errors['start_time_day_4'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_4 is None:
                    errors['end_time_day_4'] = 'این مقدار نمی تواند خالی باشد.'
            if self.day_5:
                if self.start_time_day_5 is None:
                    errors['start_time_day_5'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_5 is None:
                    errors['end_time_day_5'] = 'این مقدار نمی تواند خالی باشد.'
            if self.day_6:
                if self.start_time_day_6 is None:
                    errors['start_time_day_6'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_6 is None:
                    errors['end_time_day_6'] = 'این مقدار نمی تواند خالی باشد.'
            if self.day_0 is False and self.day_1 is False and self.day_2 is False and self.day_3 is False and self.day_4 is False and self.day_5 is False and self.day_6 is False:
                errors['datetime_type'] = 'با توجه به اینکه برنامه هفتگی است، حداقل یک روز هفته را انتخاب نمایید.'

            if self.start_date is None:
                errors['start_date'] = 'این مقدار نمی تواند خالی باشد.'
            if self.end_date is None:
                errors['end_date'] = 'این مقدار نمی تواند خالی باشد.'

        def validate_weekly_not_occasional():
            if self.specified_date is not None:
                errors['specified_date'] = 'تاریخ در برنامه های هفتگی نباید وارد شود.'
            if self.specified_start_time is not None:
                errors['specified_start_time'] = 'ساعت در برنامه های هفتگی نباید وارد شود.'
            if self.specified_end_time is not None:
                errors['specified_end_time'] = 'ساعت در برنامه های هفتگی نباید وارد شود.'

        def validate_occasional():
            if self.specified_date is None:
                errors['specified_date'] = 'با توجه به اینکه برنامه مناسبتی است، باید حداقل یک تاریخ وارد نمایید.'
            if self.specified_start_time is None:
                errors['specified_start_time'] = 'با توجه به اینکه برنامه مناسبتی است، باید حداقل یک ساعت وارد نمایید.'
            if self.specified_end_time is None:
                errors['specified_end_time'] = 'با توجه به اینکه برنامه مناسبتی است، باید حداقل یک ساعت وارد نمایید.'

        def validate_occasional_not_weekly():
            if self.day_0:
                errors['day_0'] = 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'
            if self.day_1:
                errors['day_1'] = 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'
            if self.day_2:
                errors['day_2'] = 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'
            if self.day_3:
                errors['day_3'] = 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'
            if self.day_4:
                errors['day_4'] = 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'
            if self.day_5:
                errors['day_5'] = 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'
            if self.day_6:
                errors['day_6'] = 'با توجه به اینکه برنامه مناسبتی است، هیچ روزی را نباید انتخاب نمایید.'
            if self.start_time_day_0 is not None:
                errors['start_time_day_0'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.end_time_day_0 is not None:
                errors['end_time_day_0'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.start_time_day_1 is not None:
                errors['start_time_day_1'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.end_time_day_1 is not None:
                errors['end_time_day_1'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.start_time_day_2 is not None:
                errors['start_time_day_2'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.end_time_day_2 is not None:
                errors['end_time_day_2'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.start_time_day_3 is not None:
                errors['start_time_day_3'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.end_time_day_3 is not None:
                errors['end_time_day_3'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.start_time_day_4 is not None:
                errors['start_time_day_4'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.end_time_day_4 is not None:
                errors['end_time_day_4'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.start_time_day_5 is not None:
                errors['start_time_day_5'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.end_time_day_5 is not None:
                errors['end_time_day_5'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.start_time_day_6 is not None:
                errors['start_time_day_6'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.end_time_day_6 is not None:
                errors['end_time_day_6'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.start_date is not None:
                errors['start_date'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'
            if self.end_date is not None:
                errors['end_date'] = 'با توجه به اینکه برنامه مناسبتی است، این مقدار باید خالی باشد.'

        def validate_audio():
            if self.voice_link is None:
                errors['voice_link'] = 'این مقدار نمی تواند خالی باشد.'
            if self.voice_stats_link is None:
                errors['voice_stats_link'] = 'این مقدار نمی تواند خالی باشد.'
            if self.voice_stats_type is None:
                errors['voice_stats_type'] = 'این مقدار نمی تواند خالی باشد.'
            try:
                if self.player_background is None:
                    errors['player_background'] = 'این مقدار نمی تواند خالی باشد.'
            except:
                errors['player_background'] = 'این مقدار نمی تواند خالی باشد.'

        def validate_audio_not_video():
            if self.video_link is not None:
                errors['video_link'] = 'این مقدار باید خالی باشد.'
            if self.video_stats_link is not None:
                errors['video_stats_link'] = 'این مقدار باید خالی باشد.'
            if self.video_stats_type is not None:
                errors['video_stats_type'] = 'این مقدار باید خالی باشد.'

        def validate_video():
            if self.video_link is None:
                errors['video_link'] = 'این مقدار نمی تواند خالی باشد.'
            if self.video_stats_link is None:
                errors['video_stats_link'] = 'این مقدار نمی تواند خالی باشد.'
            if self.video_stats_type is None:
                errors['video_stats_type'] = 'این مقدار نمی تواند خالی باشد.'

        def validate_video_not_audio():
            if self.voice_link is not None:
                errors['voice_link'] = 'این مقدار باید خالی باشد.'
            if self.voice_stats_link is not None:
                errors['voice_stats_link'] = 'این مقدار باید خالی باشد.'
            if self.voice_stats_type is not None:
                errors['voice_stats_type'] = 'این مقدار باید خالی باشد.'
            try:
                if self.player_background is not None:
                    errors['player_background'] = 'پخش زنده تصویری به پس زمینه نیاز ندارد.'
            except:
                errors['player_background'] = 'پخش زنده تصویری به پس زمینه نیاز ندارد.'

        logo_ratio = self.logo.height / self.logo.width
        if logo_ratio != 1:
            errors[
                'logo'] = 'نسبت اندازه های لوگو باید 1:1 باشد. برای تغییر سایز می توانید از سایت https://resizeimage.net کمک بگیرید.'
        if self.logo.size > 256000:
            errors['logo'] = 'حداکثر اندازه قابل قبول برای لوگو 250Kb است.'

        try:
            player_background_ratio = self.player_background.height / self.player_background.width
            if player_background_ratio < 1.76 or player_background_ratio > 1.78:
                errors[
                    'player_background'] = 'نسبت اندازه های پس زمینه پخش زنده باید 16:9 باشد. برای تغییر سایز می توانید از سایت https://resizeimage.net کمک بگیرید.'
            if self.player_background.size > 256000:
                errors['player_background'] = 'حداکثر اندازه قابل قبول برای پس زمینه پخش زنده 250Kb است.'
        except:
            pass

        if self.datetime_type == 'weekly':
            validate_weekly()
            validate_weekly_not_occasional()

        elif self.datetime_type == 'occasional':
            validate_occasional()
            validate_occasional_not_weekly()

        else:
            validate_weekly()
            validate_occasional()

        if self.stream_type == 'audio':
            validate_audio()
            validate_audio_not_video()
        elif self.stream_type == 'video':
            validate_video()
            validate_video_not_audio()
        else:
            validate_audio()
            validate_video()

        raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Program, self).save(*args, **kwargs)


class Menu(models.Model):
    class Meta:
        verbose_name = 'منو'
        verbose_name_plural = 'منو ها'

    title = models.CharField(max_length=20, verbose_name='عنوان')
    page_url = models.URLField(verbose_name='آدرس صفحه')
    num_order = models.PositiveSmallIntegerField(unique=True, verbose_name='ترتیب')
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False, verbose_name='سازنده',
                                related_name='created_by_menu')
    latest_modifier = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False,
                                        verbose_name='آخرین تغییر دهنده', related_name='last_modified_by_menu')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییر')

    def __str__(self):
        return self.title
