# scheduler/admin.py
from django.contrib import admin
from .models import Song, Schedule

admin.site.site_header = "Administration de la radio"
admin.site.site_title = "Administration de la radio"
admin.site.index_title = "Bienvenue sur l'administration de la radio"


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'file_path', 'created_at')
    search_fields = ('title', 'artist')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('song', 'scheduled_date', 'start_time', 'end_time', 'mount_state', 'created_at')
    list_filter = ('scheduled_date', 'mount_state')
    search_fields = ('song__title', 'song__artist')



