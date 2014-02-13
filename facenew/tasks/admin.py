
from django.contrib import admin
from facenew.tasks.models import Message
from facenew.tasks.models import UserCrontabSchedule


class MessageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('caption', 'description', 'message', 'image', 'date', 'crontab', 'enabled')
        }),
    )

    list_display = ('caption', 'description', 'enabled')



class UserCrontabScheduleAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_edit_permission(self, request):
        return False

    def has_delete_permission(self, request):
        return False

    pass

    
admin.site.register(Message, MessageAdmin)
admin.site.register(UserCrontabSchedule, UserCrontabScheduleAdmin)
