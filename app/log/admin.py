from django.contrib import admin
from .models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = [
        'description',
        'details',
        'level',
        'origin',
        'events',
        'created_at',
        'archived',
    ]


admin.site.register(Log, LogAdmin)
