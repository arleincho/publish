from django.contrib import admin

from import_export.admin import ImportExportMixin

from .models import Telephone
from .models import Account
from .models import MessagesPhoneWhatsapp


class TelephoneAdmin(ImportExportMixin, admin.ModelAdmin):
    list_filter = ['base', 'exists', 'busy', 'updated']
    list_display = ['phone', 'base', 'exists', 'busy', 'updated', 'last_seen']



class AccountAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['cc', 'phone', 'identifier', 'enabled']	



class MessagesPhoneWhatsappAdmin(admin.ModelAdmin):

    list_display = ('phone', 'message', 'message_whatsapp_id', 'sended', 'sended_at')

    def has_add_permission(self, request):
        return False



admin.site.register(MessagesPhoneWhatsapp, MessagesPhoneWhatsappAdmin)
admin.site.register(Telephone, TelephoneAdmin)
admin.site.register(Account, AccountAdmin)