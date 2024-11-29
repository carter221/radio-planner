from django.contrib import admin
from .models import CronTask

@admin.register(CronTask)
class CronTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'schedule', 'command', 'enabled')
    list_editable = ('enabled',)
    search_fields = ('name', 'command')
