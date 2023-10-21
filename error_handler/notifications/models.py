from django.db import models
from django_extensions.db.models import TimeStampedModel


class Notification(TimeStampedModel):
    class NotificationProviders(models.TextChoices):
        site = "error_handler.notifications.providers.site", "site"
        email = "error_handler.notifications.providers.email", "email"
        telegram = "error_handler.notifications.providers.telegram", "telegram"

    title = models.CharField(max_length=255)
    body = models.TextField(max_length=5000, null=True, blank=True)
    provider = models.CharField(choices=NotificationProviders.choices)
    meta = models.JSONField(null=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.title
