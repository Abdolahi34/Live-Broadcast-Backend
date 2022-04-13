from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from Programs import models


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    search_fields = ['title', 'page_url']
    list_per_page = 20
    list_display = ['title', 'page_url', 'num_order']
    list_editable = ['num_order']
    list_display_links = ['title']
    ordering = ['num_order']


@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_filter = ['stream_type', 'voice_stats_type', 'video_stats_type', 'creator', 'latest_modifier']
    search_fields = ['title', 'description', 'title_in_player', 'description_in_player', 'slug', 'logo_onclick_link',
                     'voice_link', 'voice_stats_link', 'video_link', 'video_stats_link', 'date_created',
                     'date_modified']
    list_per_page = 20
    list_display = [
        'title',
        'slug',
        'stream_type',
        'date_created',
        'creator',
        'date_modified',
        'latest_modifier',
    ]
    ordering = ['-id']

    def save_model(self, request, obj, form, change):
        if obj.creator_id is None:
            obj.creator = request.user
        obj.latest_modifier = request.user
        super(ProgramAdmin, self).save_model(request, obj, form, change)
