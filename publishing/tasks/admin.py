from django.contrib import admin
from django.contrib.flatpages.models import FlatPage 
class FlatPageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('url', 'title', 'content', 'sites')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('enable_comments', 'registration_required', 'template_name')
        }),
    )
admin.site.register(FlatPage, FlatPageAdmin)