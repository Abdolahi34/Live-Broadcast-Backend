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
        # set Creator and Latest Modifier
        if obj.creator_id is None:
            obj.creator = request.user
        obj.latest_modifier = request.user
        # End set Creator and Latest Modifier
        super(ProgramAdmin, self).save_model(request, obj, form, change)
