from django.contrib import admin
from facenew.tasks.models import Message

class MessageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('caption', 'description', 'message', 'image', 'date', 'crontab', 'enabled')
        }),
    )

    list_display = ('caption', 'description', 'enabled')

admin.site.register(Message, MessageAdmin)