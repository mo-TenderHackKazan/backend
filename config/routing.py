from django.urls import re_path

from error_handler.notifications.providers.site.consumers import NotificationsConsumer

websocket_urlpatterns = [
    re_path(r"ws/notifications/", NotificationsConsumer.as_asgi()),
]
