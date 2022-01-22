from django.contrib import admin
from . import models


class ProgramAdmin(admin.ModelAdmin):
    list_filter = ['is_active', 'created_by', 'last_modified_by']
    search_fields = ['title', 'slug', 'start_time', 'end_time', 'logo_link', 'date_created']
    list_per_page = 20
    list_display = [
        'title',
        'slug',
        'date_type',
        'start_time',
        'end_time',
        'stream',
        'date_created',
        'created_by',
        'last_modified_by',
        'is_active',
    ]

    def save_model(self, request, obj, form, change):
        if obj.created_by_id is None:
            obj.created_by = request.user
        obj.last_modified_by = request.user
        super(ProgramAdmin, self).save_model(request, obj, form, change)



class StreamTypeAdmin(admin.ModelAdmin):
    list_filter = ['stream_type']
    search_fields = ['voice_content', 'video_content']
    list_per_page = 20
    list_display = [
        'stream_type',
        'voice_content',
        'video_content',
    ]


class VideoContentAdmin(admin.ModelAdmin):
    search_fields = ['video_link', 'video_stat']
    list_per_page = 20
    list_display = [
        'video_link',
        'video_stat',
    ]


class VideoStatAdmin(admin.ModelAdmin):
    list_filter = ['video_stat_type']
    search_fields = ['video_stat_link']
    list_per_page = 20
    list_display = [
        'video_stat_link',
        'video_stat_type',
    ]


class VoiceContentAdmin(admin.ModelAdmin):
    search_fields = ['voice_link', 'voice_stat']  # TODO
    list_per_page = 20
    list_display = [
        'voice_link',
        'voice_stat',
    ]


class VoiceStatAdmin(admin.ModelAdmin):
    list_filter = ['voice_stat_type']
    search_fields = ['voice_stat_link']
    list_per_page = 20
    list_display = [
        'voice_stat_link',
        'voice_stat_type',
    ]


class DateTypeAdmin(admin.ModelAdmin):
    list_filter = ['day_type', 'day']
    search_fields = ['specified_date']
    list_per_page = 20
    list_display = [
        'day_type',
        'day',
        'specified_date',
    ]


admin.site.register(models.Program, ProgramAdmin)
admin.site.register(models.StreamType, StreamTypeAdmin)
admin.site.register(models.VideoContent, VideoContentAdmin)
admin.site.register(models.VideoStat, VideoStatAdmin)
admin.site.register(models.VoiceContent, VoiceContentAdmin)
admin.site.register(models.VoiceStat, VoiceStatAdmin)
admin.site.register(models.DateType, DateTypeAdmin)
