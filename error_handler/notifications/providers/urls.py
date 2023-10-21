from django.urls import include, path

app_name = "notifications"
urlpatterns = [
    path(
        "site/",
        include("error_handler.notifications.providers.site.urls", namespace="site"),
    ),
]
