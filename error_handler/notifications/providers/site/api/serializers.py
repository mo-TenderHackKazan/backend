from rest_framework import serializers

from error_handler.notifications.models import Notification


class SiteNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["title", "body", "created", "delivered"]
