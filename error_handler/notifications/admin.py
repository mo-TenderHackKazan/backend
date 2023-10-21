from django.contrib import admin

from error_handler.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_filter = ["provider"]
