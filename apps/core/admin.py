from django.contrib import admin

from core.models import NotificationsModel


class NotificationsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'created_date']
    list_display = ['title', 'created_date']
    list_filter = ('is_active',)
admin.site.register(NotificationsModel, NotificationsAdmin)

