
from django.contrib import admin
from facenew.tasks.models import Message
from facenew.tasks.models import UserCrontabSchedule


class MessageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('caption', 'description', 'message', 'link', 'image', 'date', 'crontab', 'enabled')
        }),
    )

    list_display = ('caption', 'description', 'enabled', 'date', 'crontab')



class UserCrontabScheduleAdmin(admin.ModelAdmin):

    list_display = ('user', 'periodic_task')

    def has_add_permission(self, request):
        return False

    pass

    
admin.site.register(Message, MessageAdmin)
admin.site.register(UserCrontabSchedule, UserCrontabScheduleAdmin)
