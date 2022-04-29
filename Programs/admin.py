from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
import datetime

from Programs import models


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    search_fields = ['title', 'page_url', 'creator', 'latest_modifier', 'date_created', 'date_modified']
    list_per_page = 20
    list_display = ['title', 'page_url', 'num_order', 'creator']
    list_editable = ['num_order']
    list_display_links = ['title']
    ordering = ['num_order']

    def save_model(self, request, obj, form, change):
        if obj.creator_id is None:
            obj.creator = request.user
        obj.latest_modifier = request.user
        super(MenuAdmin, self).save_model(request, obj, form, change)


@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_filter = ['status', 'datetime_type', 'stream_type', 'voice_stats_type', 'video_stats_type', 'day_0', 'day_1',
                   'day_2', 'day_3', 'day_4', 'day_5', 'day_6', ]
    search_fields = ['title', 'description', 'title_in_player', 'description_in_player', 'slug', 'date_display',
                     'time_display', 'start_time_day_0', 'end_time_day_0', 'start_time_day_1', 'end_time_day_1',
                     'start_time_day_2', 'end_time_day_2', 'start_time_day_3', 'end_time_day_3', 'start_time_day_4',
                     'end_time_day_4', 'start_time_day_5', 'end_time_day_5', 'start_time_day_6', 'end_time_day_6',
                     'start_date', 'end_date', 'specified_date', 'specified_start_time', 'specified_end_time',
                     'logo_link', 'voice_link', 'voice_stats_link', 'video_link', 'video_stats_link',
                     'creator', 'latest_modifier', 'date_created', 'date_modified']
    list_per_page = 20
    list_display = [
        'title',
        'slug',
        'date_display',
        'time_display',
        'stream_type',
        'status',
        'date_created',
        'creator',
        'date_modified',
        'latest_modifier',
    ]
    ordering = ['-id']

    def save_model(self, request, obj, form, change):
        def timestamps_weekly_func():
            def append_days_timestamps_func(start_date, start_time, end_time):
                while start_date <= obj.end_date:
                    this_timestamp_start = datetime.datetime(start_date.year, start_date.month, start_date.day,
                                                             start_time.hour, start_time.minute,
                                                             start_time.second, 0).timestamp()
                    this_timestamp_end = datetime.datetime(obj.end_date.year, obj.end_date.month,
                                                           obj.end_date.day, end_time.hour, end_time.minute,
                                                           end_time.second, 0).timestamp()
                    obj.timestamps_start_weekly.append(this_timestamp_start)
                    obj.timestamps_end_weekly.append(this_timestamp_end)
                    start_date = datetime.timedelta(days=7)

            if obj.start_date <= datetime.datetime.now().date():
                now_weekday = datetime.datetime.now().weekday()
                if obj.day_0:
                    now_date = datetime.datetime.now().date()
                    if now_weekday != 5:
                        now_date += datetime.timedelta(days=now_weekday - 5)
                    append_days_timestamps_func(now_date, obj.start_time_day_0, obj.end_time_day_0)
                if obj.day_1:
                    now_date = datetime.datetime.now().date()
                    if now_weekday != 6:
                        now_date += datetime.timedelta(days=now_weekday - 6)
                    append_days_timestamps_func(now_date, obj.start_time_day_1, obj.end_time_day_1)
                if obj.day_2:
                    now_date = datetime.datetime.now().date()
                    if now_weekday != 0:
                        now_date += datetime.timedelta(days=now_weekday - 0)
                    append_days_timestamps_func(now_date, obj.start_time_day_2, obj.end_time_day_2)
                if obj.day_3:
                    now_date = datetime.datetime.now().date()
                    if now_weekday != 1:
                        now_date += datetime.timedelta(days=now_weekday - 1)
                    append_days_timestamps_func(now_date, obj.start_time_day_3, obj.end_time_day_3)
                if obj.day_4:
                    now_date = datetime.datetime.now().date()
                    if now_weekday != 2:
                        now_date += datetime.timedelta(days=now_weekday - 2)
                    append_days_timestamps_func(now_date, obj.start_time_day_4, obj.end_time_day_4)
                if obj.day_5:
                    now_date = datetime.datetime.now().date()
                    if now_weekday != 3:
                        now_date += datetime.timedelta(days=now_weekday - 3)
                    append_days_timestamps_func(now_date, obj.start_time_day_5, obj.end_time_day_5)
                if obj.day_6:
                    now_date = datetime.datetime.now().date()
                    if now_weekday != 4:
                        now_date += datetime.timedelta(days=now_weekday - 4)
                    append_days_timestamps_func(now_date, obj.start_time_day_6, obj.end_time_day_6)
            else:
                if obj.day_0:
                    append_days_timestamps_func(obj.end_date, obj.start_time_day_0, obj.end_time_day_0)
                if obj.day_1:
                    append_days_timestamps_func(obj.end_date, obj.start_time_day_1, obj.end_time_day_1)
                if obj.day_2:
                    append_days_timestamps_func(obj.end_date, obj.start_time_day_2, obj.end_time_day_2)
                if obj.day_3:
                    append_days_timestamps_func(obj.end_date, obj.start_time_day_3, obj.end_time_day_3)
                if obj.day_4:
                    append_days_timestamps_func(obj.end_date, obj.start_time_day_4, obj.end_time_day_4)
                if obj.day_5:
                    append_days_timestamps_func(obj.end_date, obj.start_time_day_5, obj.end_time_day_5)
                if obj.day_6:
                    append_days_timestamps_func(obj.end_date, obj.start_time_day_6, obj.end_time_day_6)

        def timestamps_occasional_func():
            i = 0
            while i != -1:
                try:
                    this_timestamp_start = datetime.datetime(obj.specified_date[i].year, obj.specified_date[i].month,
                                                             obj.specified_date[i].day,
                                                             obj.specified_start_time[i].hour,
                                                             obj.specified_start_time[i].minute,
                                                             obj.specified_start_time[i].second, 0).timestamp()
                    this_timestamp_end = datetime.datetime(obj.specified_date[i].year, obj.specified_date[i].month,
                                                           obj.specified_date[i].day,
                                                           obj.specified_end_time[i].hour,
                                                           obj.specified_end_time[i].minute,
                                                           obj.specified_end_time[i].second, 0).timestamp()
                    obj.timestamps_start_occasional.append(this_timestamp_start)
                    obj.timestamps_end_occasional.append(this_timestamp_end)
                    i += 1
                except:
                    i = -1

        # set Creator and Latest Modifier
        if obj.creator_id is None:
            obj.creator = request.user
        obj.latest_modifier = request.user
        # End set Creator and Latest Modifier

        if obj.datetime_type == 'weekly':
            obj.timestamps_start_weekly = []
            obj.timestamps_end_weekly = []
            timestamps_weekly_func()
        elif obj.datetime_type == 'occasional':
            obj.timestamps_start_occasional = []
            obj.timestamps_end_occasional = []
            timestamps_occasional_func()
        else:
            obj.timestamps_start_weekly = []
            obj.timestamps_end_weekly = []
            timestamps_weekly_func()
            obj.timestamps_start_occasional = []
            obj.timestamps_end_occasional = []
            timestamps_occasional_func()

        super(ProgramAdmin, self).save_model(request, obj, form, change)
