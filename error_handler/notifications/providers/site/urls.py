from django.urls import path

from error_handler.notifications.providers.site.api.views import (
    ListNotificationsAPIView,
)

app_name = "notifications:site"
urlpatterns = [
    path("", ListNotificationsAPIView.as_view(), name="list"),
]
