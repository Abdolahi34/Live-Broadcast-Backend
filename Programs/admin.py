from django.contrib import admin

from Programs import models


@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin):
    list_filter = ['is_active', 'created_by', 'last_modified_by']
    search_fields = ['title', 'slug', 'start_time', 'end_time', 'logo', 'date_created', 'date_modified']
    list_per_page = 20
    list_display = [
        'num_order',
        'title',
        'slug',
        'datetype',
        'start_time',
        'end_time',
        'stream',
        'date_created',
        'created_by',
        'date_modified',
        'last_modified_by',
        'is_active',
    ]
    list_editable = ['num_order']
    list_display_links = ['title']
    ordering = ['num_order']

    def save_model(self, request, obj, form, change):
        if obj.created_by_id is None:
            obj.created_by = request.user
        obj.last_modified_by = request.user
        super(ProgramAdmin, self).save_model(request, obj, form, change)


@admin.register(models.StreamType)
class StreamTypeAdmin(admin.ModelAdmin):
    list_filter = ['stream_type']
    search_fields = ['voice_content', 'video_content']
    list_per_page = 20
    list_display = [
        'stream_type',
        'voice_content',
        'video_content',
    ]
    ordering = ['-id']


@admin.register(models.VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    search_fields = ['video_link', 'video_stat']
    list_per_page = 20
    list_display = [
        'video_link',
        'video_stat',
    ]
    ordering = ['-id']


@admin.register(models.VideoStat)
class VideoStatAdmin(admin.ModelAdmin):
    list_filter = ['video_stat_type']
    search_fields = ['video_stat_link']
    list_per_page = 20
    list_display = [
        'video_stat_link',
        'video_stat_type',
    ]
    ordering = ['-id']


@admin.register(models.VoiceContent)
class VoiceContentAdmin(admin.ModelAdmin):
    search_fields = ['voice_link', 'voice_stat']
    list_per_page = 20
    list_display = [
        'voice_link',
        'voice_stat',
    ]
    ordering = ['-id']


@admin.register(models.VoiceStat)
class VoiceStatAdmin(admin.ModelAdmin):
    list_filter = ['voice_stat_type']
    search_fields = ['voice_stat_link']
    list_per_page = 20
    list_display = [
        'voice_stat_link',
        'voice_stat_type',
    ]
    ordering = ['-id']


@admin.register(models.DateType)
class DateTypeAdmin(admin.ModelAdmin):
    list_filter = ['day_type', 'day']
    search_fields = ['specified_date']
    list_per_page = 20
    list_display = [
        'day_type',
        'day',
        'specified_date',
    ]
    ordering = ['-id']
