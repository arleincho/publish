from django.contrib import admin

from import_export.admin import ImportExportMixin

from .models import Telephone
from .models import Account


class TelephoneAdmin(ImportExportMixin, admin.ModelAdmin):
    list_filter = ['base', 'exists', 'updated']
    list_display = ['phone', 'base', 'exists', 'busy', 'updated']


class AccountAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['cc', 'phone', 'identifier', 'enabled']	


admin.site.register(Telephone, TelephoneAdmin)
admin.site.register(Account, AccountAdmin)