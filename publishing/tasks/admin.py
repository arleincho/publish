from django.contrib import admin
from publishing.tasks.models import Message

class MessageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('caption', 'description', 'message', 'image', 'enabled')
        }),
    )

    list_display = ('caption', 'description', 'enabled')

admin.site.register(Message, MessageAdmin)