
from django.contrib import admin
from facenew.tasks.models import Message
from facenew.tasks.models import UserCrontabSchedule
from facenew.whatsapp.models import MessagesPhoneWhatsapp


class MessageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('caption', 'description', 'type_message', 'message', 'link', 'image', 'date', 'crontab', 'enabled')
        }),
    )

    list_display = ('caption', 'description', 'type_message', 'enabled', 'date', 'crontab')



class MessagesPhoneWhatsappAdmin(admin.ModelAdmin):

    list_display = ('user', 'periodic_task')

    def has_add_permission(self, request):
        return False

class MessagesTelephoneAdmin(admin.ModelAdmin):

    list_display = ('phone', 'message', 'sended', 'sended_at')

    def has_add_permission(self, request):
        return False

admin.site.register(MessagesPhoneWhatsapp, MessagesPhoneWhatsappAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserCrontabSchedule, UserCrontabScheduleAdmin)
