'''
توضیحات هر فیلد در verbose_name همان فیلد نوشته شده است.

سیستم بوسیله datetime_type تشخیص میدهد که برنامه به چه صورتی است.
1- اگر برنامه هفتگی بود، هنگام ذخیره کردن برنامه، بین start_date و end_date (که تاریخ شروع و پایان برنامه هفتگی است)،
طبق روز های انتخابی و اطلاعات ورودی، تمام برنامه ها را پیدا و تایم استمپ آنها را در timestamps_start_weekly و timestamps_end_weekly ذخیره میکند.
(این 2 فیلد به ترتیب لیست هایی از تایم استمپ های شروع و پایان برنامه های هفتگی یک instance از program هستند.)
در زمان اجرای فرمان set_timestamps در ویوها هم،
تایم استمپ های شروع و پایان هر برنامه را به همان ترتیب در timestamps_start_weekly و timestamps_end_weekly ثبت میکند.
2- اگر برنامه مناسبتی بود، فیلد های specified_date و specified_start_time و specified_end_time به ترتیب تاریخ ها،
زمان های شروع و زمان های پایان یک برنامه مناسبتی هستند. مثلا مورد های اول هرکدام از لیست ها، اطلاعات مربوط به یک برنامه هستند.
هنگام ذخیره برنامه مناسبتی و یا اجرای فرمان set_timestamps در ویوها،
timestamps_start_occasional و timestamps_end_occasional از تایم استمپ های برنامه ها تکمیل خواهند شد.
3- اگر برنامه هفتگی - مناسبتی بود (این سبک برنامه سبکی ترکیبی است، به این صورت که برنامه ای هفتگی، چند جلسه علاوه بر سیکل معمولی اش در چند تاریخ دیگر هم برگزار شود)،
هم فیلد های تایم استمپ هفتگی و هم مناسبتی، هنگام ذخیره یا اجرای فرمان set_timestamps در ویوها، تکمیل می گردند.
'''
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
import datetime
import logging

logger = logging.getLogger(__name__)


class Program(models.Model):
    class Meta:
        verbose_name = 'برنامه'
        verbose_name_plural = 'برنامه ها'

    status_choices = (
        ('publish', 'انتشار'),
        ('draft', 'پیش نویس'),
        ('archive', 'بایگانی'),
    )

    datetime_type_choices = (
        ('weekly', 'هفتگی'),
        ('occasional', 'مناسبتی'),
        ('weekly_occasional', 'هفتگی - مناسبتی'),
    )

    stream_type_choices = (
        ('audio', 'صوتی'),
        ('video', 'تصویری'),
        ('audio_video', 'صوتی و تصویری'),
    )

    audio_platform_type_choices = (
        ('shoutcast', 'Shoutcast'),
        ('wowza', 'Wowza'),
    )

    video_platform_type_choices = (
        ('wowza', 'Wowza'),
    )

    status = models.CharField(max_length=7, choices=status_choices, db_index=True, verbose_name='وضعیت برنامه')
    title = models.CharField(max_length=50, help_text='تعداد کاراکتر مجاز 50 عدد می باشد.', verbose_name='عنوان')
    description = models.TextField(max_length=250, help_text='تعداد کاراکتر مجاز 250 عدد می باشد.',
                                   verbose_name='توضیحات')
    title_in_player = models.CharField(max_length=50, help_text='تعداد کاراکتر مجاز 50 عدد می باشد.',
                                       verbose_name='عنوان در صفحه پخش زنده')
    description_in_player = models.TextField(max_length=250, help_text='تعداد کاراکتر مجاز 250 عدد می باشد.',
                                             verbose_name='توضیحات در صفحه پخش زنده')
    slug = models.SlugField(max_length=70, help_text='تعداد کاراکتر مجاز 70 عدد می باشد.', unique=True,
                            verbose_name='Slug')
    date_display = models.CharField(max_length=30, help_text='تعداد کاراکتر مجاز 30 عدد می باشد.',
                                    verbose_name='تاریخ نمایش داده شده به کاربر')
    time_display = models.CharField(max_length=30, help_text='تعداد کاراکتر مجاز 30 عدد می باشد.',
                                    verbose_name='ساعت نمایش داده شده به کاربر')
    datetime_type = models.CharField(max_length=17, choices=datetime_type_choices, verbose_name='نوع برگزاری برنامه')
    start_date = models.DateField(blank=True, null=True, verbose_name='تاریخ شروع برنامه هفتگی',
                                  help_text='تاریخ به فرمت (01-01-2022) باید وارد شود')
    end_date = models.DateField(blank=True, null=True, verbose_name='تاریخ پایان برنامه هفتگی',
                                help_text='تاریخ به فرمت (01-01-2022) باید وارد شود')
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
    # When the set_timestamps command is executed in the views, the earliest timestamp is completed with the lowest timestamp (closest).
    timestamp_earliest = models.PositiveBigIntegerField(blank=True, null=True, editable=False, default=0)
    logo = models.ImageField(upload_to='api/program/logo/',
                             help_text='نسبت طول و عرض لوگو باید 1:1 باشد. (حداکثر سایز 250KB)',
                             verbose_name='لوگو')
    # The link displayed on the program page
    logo_link = models.URLField(default='https://lesansedgh.ir',
                                help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                verbose_name='لینک لوگو')
    # program background image (for audio program)
    player_background = models.ImageField(upload_to='api/program/player_background/', blank=True, null=True,
                                          help_text='نسبت طول و عرض تصویر پس زمینه پخش زنده باید 16:9 باشد. (حداکثر سایز 250KB)',
                                          verbose_name='تصویر پس زمینه پخش زنده')
    stream_type = models.CharField(max_length=11, choices=stream_type_choices, verbose_name='نوع پخش زنده')
    audio_link = models.URLField(blank=True, null=True, help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                 verbose_name='لینک پخش زنده صوتی')
    audio_stats_link = models.URLField(blank=True, null=True, help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                       verbose_name='لینک آمار پخش زنده صوتی')
    audio_platform_type = models.CharField(blank=True, null=True, max_length=9, choices=audio_platform_type_choices,
                                           verbose_name='نوع پلتفرم پخش زنده صوتی')
    video_link = models.URLField(blank=True, null=True, help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                 verbose_name='لینک پخش زنده تصویری')
    video_stats_link = models.URLField(blank=True, null=True, help_text='تعداد کاراکتر مجاز 200 عدد می باشد.',
                                       verbose_name='لینک آمار پخش زنده تصویری')
    video_platform_type = models.CharField(blank=True, null=True, max_length=9, choices=video_platform_type_choices,
                                           verbose_name='نوع پلتفرم پخش زنده تصویری')
    is_on_planning = models.BooleanField(default=False,
                                         editable=False)  # True, if we are between the start and end times of the program
    is_audio_active = models.BooleanField(default=False, editable=False)  # True, if audio_link is active
    is_video_active = models.BooleanField(default=False, editable=False)  # True, if video_link is active
    isLive = models.BooleanField(default=False, editable=False,
                                 verbose_name='زنده')  # True, if audio_link or video_link is active
    # Every 10 seconds, a command is executed that adds a number to error_count if the program is interrupted suddenly. error_count can be between 0 and 4.
    error_count = models.PositiveSmallIntegerField(default=0, editable=False)
    """
    A message is sent to the channel when we enter the program's time limit, and a message is sent to the channel when audio or video links are activated.
    0 = Program not started
    10 = on start time message sent
    11 = on start time and start program message sent
    """
    send_message = models.PositiveSmallIntegerField(default=0, editable=False)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False, verbose_name='سازنده',
                                related_name='creator_program')
    latest_modifier = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False,
                                        verbose_name='آخرین تغییر دهنده', related_name='last_modified_by_program')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییر')

    def __str__(self):
        return self.title

    # Validation of information sent by the user
    def clean(self):
        errors = {}

        # Validation when It must be weekly
        def validate_weekly():
            if self.day_0:
                if self.start_time_day_0 is None:
                    errors['start_time_day_0'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_0 is None:
                    errors['end_time_day_0'] = 'این مقدار نمی تواند خالی باشد.'
            else:
                if self.start_time_day_0 is not None:
                    errors['start_time_day_0'] = 'این مقدار باید خالی باشد.'
                if self.end_time_day_0 is not None:
                    errors['end_time_day_0'] = 'این مقدار باید خالی باشد.'
            if self.day_1:
                if self.start_time_day_1 is None:
                    errors['start_time_day_1'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_1 is None:
                    errors['end_time_day_1'] = 'این مقدار نمی تواند خالی باشد.'
            else:
                if self.start_time_day_1 is not None:
                    errors['start_time_day_1'] = 'این مقدار باید خالی باشد.'
                if self.end_time_day_1 is not None:
                    errors['end_time_day_1'] = 'این مقدار باید خالی باشد.'
            if self.day_2:
                if self.start_time_day_2 is None:
                    errors['start_time_day_2'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_2 is None:
                    errors['end_time_day_2'] = 'این مقدار نمی تواند خالی باشد.'
            else:
                if self.start_time_day_2 is not None:
                    errors['start_time_day_2'] = 'این مقدار باید خالی باشد.'
                if self.end_time_day_2 is not None:
                    errors['end_time_day_2'] = 'این مقدار باید خالی باشد.'
            if self.day_3:
                if self.start_time_day_3 is None:
                    errors['start_time_day_3'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_3 is None:
                    errors['end_time_day_3'] = 'این مقدار نمی تواند خالی باشد.'
            else:
                if self.start_time_day_3 is not None:
                    errors['start_time_day_3'] = 'این مقدار باید خالی باشد.'
                if self.end_time_day_3 is not None:
                    errors['end_time_day_3'] = 'این مقدار باید خالی باشد.'
            if self.day_4:
                if self.start_time_day_4 is None:
                    errors['start_time_day_4'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_4 is None:
                    errors['end_time_day_4'] = 'این مقدار نمی تواند خالی باشد.'
            else:
                if self.start_time_day_4 is not None:
                    errors['start_time_day_4'] = 'این مقدار باید خالی باشد.'
                if self.end_time_day_4 is not None:
                    errors['end_time_day_4'] = 'این مقدار باید خالی باشد.'
            if self.day_5:
                if self.start_time_day_5 is None:
                    errors['start_time_day_5'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_5 is None:
                    errors['end_time_day_5'] = 'این مقدار نمی تواند خالی باشد.'
            else:
                if self.start_time_day_5 is not None:
                    errors['start_time_day_5'] = 'این مقدار باید خالی باشد.'
                if self.end_time_day_5 is not None:
                    errors['end_time_day_5'] = 'این مقدار باید خالی باشد.'
            if self.day_6:
                if self.start_time_day_6 is None:
                    errors['start_time_day_6'] = 'این مقدار نمی تواند خالی باشد.'
                if self.end_time_day_6 is None:
                    errors['end_time_day_6'] = 'این مقدار نمی تواند خالی باشد.'
            else:
                if self.start_time_day_6 is not None:
                    errors['start_time_day_6'] = 'این مقدار باید خالی باشد.'
                if self.end_time_day_6 is not None:
                    errors['end_time_day_6'] = 'این مقدار باید خالی باشد.'
            if self.day_0 is False and self.day_1 is False and self.day_2 is False and self.day_3 is False and self.day_4 is False and self.day_5 is False and self.day_6 is False:
                errors['datetime_type'] = 'با توجه به اینکه برنامه هفتگی است، حداقل یک روز هفته را انتخاب نمایید.'

            if self.start_date is None:
                errors['start_date'] = 'این مقدار نمی تواند خالی باشد.'
            if self.end_date is None:
                errors['end_date'] = 'این مقدار نمی تواند خالی باشد.'

        # Validation when It must not be an occasion (for weekly programs)
        def validate_not_occasional():
            if self.specified_date:
                errors['specified_date'] = 'تاریخ در برنامه های هفتگی نباید وارد شود.'
            if self.specified_start_time:
                errors['specified_start_time'] = 'ساعت در برنامه های هفتگی نباید وارد شود.'
            if self.specified_end_time:
                errors['specified_end_time'] = 'ساعت در برنامه های هفتگی نباید وارد شود.'

        # Validation when It must be an occasion
        def validate_occasional():
            if self.specified_date is None:
                errors['specified_date'] = 'با توجه به اینکه برنامه مناسبتی است، باید حداقل یک تاریخ وارد نمایید.'
            if self.specified_start_time is None:
                errors['specified_start_time'] = 'با توجه به اینکه برنامه مناسبتی است، باید حداقل یک ساعت وارد نمایید.'
            if self.specified_end_time is None:
                errors['specified_end_time'] = 'با توجه به اینکه برنامه مناسبتی است، باید حداقل یک ساعت وارد نمایید.'
            if len(self.specified_date) != len(self.specified_start_time):
                errors['specified_date'] = 'در برنامه های مناسبتی تعداد تاریخ و ساعت ها باید یکسان باشد.'
                errors['specified_start_time'] = 'در برنامه های مناسبتی تعداد تاریخ و ساعت ها باید یکسان باشد.'
            if len(self.specified_date) != len(self.specified_end_time):
                errors['specified_date'] = 'در برنامه های مناسبتی تعداد تاریخ و ساعت ها باید یکسان باشد.'
                errors['specified_end_time'] = 'در برنامه های مناسبتی تعداد تاریخ و ساعت ها باید یکسان باشد.'
            if len(self.specified_start_time) != len(self.specified_end_time):
                errors['specified_start_time'] = 'در برنامه های مناسبتی تعداد تاریخ و ساعت ها باید یکسان باشد.'
                errors['specified_end_time'] = 'در برنامه های مناسبتی تعداد تاریخ و ساعت ها باید یکسان باشد.'

        # Validation when It must not be weekly (for occasion programs)
        def validate_not_weekly():
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

        # Validation when The program must be audio
        def validate_audio():
            if self.audio_link is None:
                errors['audio_link'] = 'این مقدار نمی تواند خالی باشد.'
            if self.audio_stats_link is None:
                errors['audio_stats_link'] = 'این مقدار نمی تواند خالی باشد.'
            if self.audio_platform_type is None:
                errors['audio_platform_type'] = 'این مقدار نمی تواند خالی باشد.'

        # Validation when The program must not be video (for audio only programs)
        def validate_not_video():
            if self.video_link is not None:
                errors['video_link'] = 'این مقدار باید خالی باشد.'
            if self.video_stats_link is not None:
                errors['video_stats_link'] = 'این مقدار باید خالی باشد.'
            if self.video_platform_type is not None:
                errors['video_platform_type'] = 'این مقدار باید خالی باشد.'

        # Validation when The program must be video
        def validate_video():
            if self.video_link is None:
                errors['video_link'] = 'این مقدار نمی تواند خالی باشد.'
            if self.video_stats_link is None:
                errors['video_stats_link'] = 'این مقدار نمی تواند خالی باشد.'
            if self.video_platform_type is None:
                errors['video_platform_type'] = 'این مقدار نمی تواند خالی باشد.'

        # Validation when The program must not be audio (for video only programs)
        def validate_not_audio():
            if self.audio_link is not None:
                errors['audio_link'] = 'این مقدار باید خالی باشد.'
            if self.audio_stats_link is not None:
                errors['audio_stats_link'] = 'این مقدار باید خالی باشد.'
            if self.audio_platform_type is not None:
                errors['audio_platform_type'] = 'این مقدار باید خالی باشد.'

        # Validation when the program must have background playback
        def validate_player_background():
            try:
                if 0 < self.player_background.height:
                    player_background_ratio = self.player_background.height / self.player_background.width
                    if player_background_ratio < 1.76 or 1.78 < player_background_ratio:
                        errors[
                            'player_background'] = 'نسبت اندازه های پس زمینه پخش زنده باید 9:16 باشد. برای تغییر سایز می توانید از سایت https://resizeimage.net کمک بگیرید.'
                    if self.player_background.size > 256000:
                        errors['player_background'] = 'حداکثر اندازه قابل قبول برای پس زمینه پخش زنده 250Kb است.'
            except Exception as e:
                logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
                errors['player_background'] = 'این مقدار نمی تواند خالی باشد.'

        # Validation when the program must not have background playback (for video only programs)
        def validate_not_player_background():
            try:
                if 0 < self.player_background.height:
                    errors['player_background'] = 'پخش زنده تصویری به پس زمینه نیاز ندارد.'
            except Exception as e:
                logger.error('The try block part encountered an error: %s', str(e), exc_info=True)

        # Logo validation
        try:
            logo_ratio = self.logo.height / self.logo.width
            if logo_ratio != 1:
                errors[
                    'logo'] = 'نسبت اندازه های لوگو باید 1:1 باشد. برای تغییر سایز می توانید از سایت https://resizeimage.net کمک بگیرید.'
            if self.logo.size > 256000:
                errors['logo'] = 'حداکثر اندازه قابل قبول برای لوگو 250Kb است.'
        except Exception as e:
            logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
            errors['logo'] = 'این مقدار نمی تواند خالی باشد.'

        # program date and time validation
        if self.datetime_type == 'weekly':
            validate_weekly()
            validate_not_occasional()
        elif self.datetime_type == 'occasional':
            validate_occasional()
            validate_not_weekly()
        else:
            validate_weekly()
            validate_occasional()

        # program stream validation
        if self.stream_type == 'audio':
            validate_audio()
            validate_player_background()
            validate_not_video()
        elif self.stream_type == 'video':
            validate_video()
            validate_not_audio()
            validate_not_player_background()
        else:
            validate_audio()
            validate_player_background()
            validate_video()

        raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()

        # TODO Synchronize the set_timestamps function with the save function of the Program model.
        def timestamps_weekly_func():
            def append_days_timestamps_func(start_date, start_time, end_time):
                while start_date <= self.end_date:
                    if datetime.datetime.now().date() == start_date and end_time < datetime.datetime.now().time():
                        start_date += datetime.timedelta(days=7)
                        continue
                    this_timestamp_start = datetime.datetime(start_date.year, start_date.month, start_date.day,
                                                             start_time.hour, start_time.minute,
                                                             start_time.second, 0).timestamp()
                    if start_time < end_time:
                        this_timestamp_end = datetime.datetime(start_date.year, start_date.month, start_date.day,
                                                               end_time.hour, end_time.minute,
                                                               end_time.second, 0).timestamp()
                    else:
                        # start_time before 12 pm and end_time after 12 pm
                        start_date += datetime.timedelta(days=1)
                        this_timestamp_end = datetime.datetime(start_date.year, start_date.month, start_date.day,
                                                               end_time.hour, end_time.minute,
                                                               end_time.second, 0).timestamp()
                        start_date -= datetime.timedelta(days=1)
                    self.timestamps_start_weekly.append(this_timestamp_start)
                    self.timestamps_end_weekly.append(this_timestamp_end)
                    start_date += datetime.timedelta(days=7)

            # create list for set timestamps
            days = [self.day_0, self.day_1, self.day_2, self.day_3, self.day_4, self.day_5,
                    self.day_6]
            start_time_days = [self.start_time_day_0, self.start_time_day_1, self.start_time_day_2,
                               self.start_time_day_3, self.start_time_day_4, self.start_time_day_5,
                               self.start_time_day_6]
            end_time_days = [self.end_time_day_0, self.end_time_day_1, self.end_time_day_2,
                             self.end_time_day_3, self.end_time_day_4, self.end_time_day_5,
                             self.end_time_day_6]

            now_date = datetime.datetime.now().date()
            now_weekday = datetime.datetime.now().isoweekday()
            iso_weekday_nums = [6, 7, 1, 2, 3, 4, 5]
            for i in range(7):
                if days[i]:
                    if now_weekday == iso_weekday_nums[i]:
                        # Set timestamps for the current day of the week that is active
                        append_days_timestamps_func(now_date, start_time_days[i], end_time_days[i])
                    else:
                        # Jump to the next day of the week that is active
                        for j in range(6):
                            now_date += datetime.timedelta(days=1)
                            if now_date.isoweekday() == iso_weekday_nums[i]:
                                append_days_timestamps_func(now_date, start_time_days[i], end_time_days[i])
                                break
                        now_date = datetime.datetime.now().date()

        def timestamps_occasional_func():
            try:
                program_len = len(self.specified_date)
                for i in range(program_len):
                    this_specified_date = self.specified_date[i]
                    this_specified_start_time = self.specified_start_time[i]
                    this_specified_end_time = self.specified_end_time[i]
                    if datetime.datetime.now().date() <= this_specified_date:
                        if datetime.datetime.now().date() == this_specified_date and this_specified_end_time < datetime.datetime.now().time():
                            continue
                        this_timestamp_start = datetime.datetime(this_specified_date.year,
                                                                 this_specified_date.month,
                                                                 this_specified_date.day,
                                                                 this_specified_start_time.hour,
                                                                 this_specified_start_time.minute,
                                                                 this_specified_start_time.second, 0).timestamp()
                        # start_time before 12 pm and end_time after 12 pm
                        if this_specified_end_time < this_specified_start_time:
                            this_specified_date += datetime.timedelta(days=1)

                        this_timestamp_end = datetime.datetime(this_specified_date.year, this_specified_date.month,
                                                               this_specified_date.day,
                                                               this_specified_end_time.hour,
                                                               this_specified_end_time.minute,
                                                               this_specified_end_time.second, 0).timestamp()
                        self.timestamps_start_occasional.append(this_timestamp_start)
                        self.timestamps_end_occasional.append(this_timestamp_end)
            except Exception as e:
                logger.error('The try block part encountered an error: %s', str(e), exc_info=True)

        if self.datetime_type == 'weekly':
            # set occasional timestamps None
            self.timestamps_start_occasional = None
            self.timestamps_end_occasional = None
            # set weekly timestamps
            self.timestamps_start_weekly = []
            self.timestamps_end_weekly = []
            timestamps_weekly_func()
        elif self.datetime_type == 'occasional':
            # set weekly timestamps None
            self.timestamps_start_weekly = None
            self.timestamps_end_weekly = None
            # set occasional timestamps
            self.timestamps_start_occasional = []
            self.timestamps_end_occasional = []
            timestamps_occasional_func()
        else:
            # set weekly timestamps
            self.timestamps_start_weekly = []
            self.timestamps_end_weekly = []
            timestamps_weekly_func()
            # set occasional timestamps
            self.timestamps_start_occasional = []
            self.timestamps_end_occasional = []
            timestamps_occasional_func()

        # Start Set_Timestamp_Earliest
        def set_outdated_program():
            self.timestamp_earliest = 0
            self.status = 'archive'

        if self.datetime_type == 'weekly':
            try:
                # اگر الان در محدوده زمانی برنامه باشیم، برنامه فعلی را هم در timestamp_earliest در نظر میگیرد
                if self.is_on_planning:
                    self.timestamp_earliest = min(self.timestamps_end_weekly)
                else:
                    self.timestamp_earliest = min(self.timestamps_start_weekly)
            except Exception as e:
                logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
                set_outdated_program()
        elif self.datetime_type == 'occasional':
            try:
                # اگر الان در محدوده زمانی برنامه باشیم، برنامه فعلی را هم در timestamp_earliest در نظر میگیرد
                if self.is_on_planning:
                    self.timestamp_earliest = min(self.timestamps_end_occasional)
                else:
                    self.timestamp_earliest = min(self.timestamps_start_occasional)
            except Exception as e:
                logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
                set_outdated_program()
            # weekly-occasional
        else:
            try:
                # اگر الان در محدوده زمانی برنامه باشیم، برنامه فعلی را هم در timestamp_earliest در نظر میگیرد
                if self.is_on_planning:
                    timestamps_weekly_earliest = min(self.timestamps_end_weekly)
                    timestamps_occasional_earliest = min(self.timestamps_end_occasional)
                    self.timestamp_earliest = min(timestamps_weekly_earliest, timestamps_occasional_earliest)
                else:
                    timestamps_weekly_earliest = min(self.timestamps_start_weekly)
                    timestamps_occasional_earliest = min(self.timestamps_start_occasional)
                    self.timestamp_earliest = min(timestamps_weekly_earliest, timestamps_occasional_earliest)
            except Exception as e:
                logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
                if not self.timestamps_start_weekly and not self.timestamps_start_occasional:
                    set_outdated_program()
                # If one of the weekly or occasional cycles is left
                else:
                    # اگر الان در محدوده زمانی برنامه باشیم، برنامه فعلی را هم در timestamp_earliest در نظر میگیرد
                    if self.is_on_planning:
                        if not self.timestamps_end_weekly:
                            self.timestamp_earliest = min(self.timestamps_end_occasional)
                        else:
                            self.timestamp_earliest = min(self.timestamps_end_weekly)
                    else:
                        if not self.timestamps_start_weekly:
                            self.timestamp_earliest = min(self.timestamps_start_occasional)
                        else:
                            self.timestamp_earliest = min(self.timestamps_start_weekly)
        # End Set_Timestamp_Earliest
        super(Program, self).save(*args, **kwargs)


class Menu(models.Model):
    class Meta:
        verbose_name = 'منو'
        verbose_name_plural = 'منو ها'

    title = models.CharField(max_length=20, verbose_name='عنوان', help_text='تعداد کاراکتر مجاز 20 عدد می باشد')
    page_url = models.URLField(verbose_name='آدرس صفحه')
    # Menu items are sorted by num_order
    num_order = models.PositiveSmallIntegerField(unique=True, verbose_name='ترتیب')
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False, verbose_name='سازنده',
                                related_name='creator_menu')
    latest_modifier = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False,
                                        verbose_name='آخرین تغییر دهنده', related_name='last_modified_by_menu')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییر')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Menu, self).save(*args, **kwargs)
