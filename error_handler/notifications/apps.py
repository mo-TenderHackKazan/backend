from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = "error_handler.notifications"
    verbose_name = "Notifications"

    def ready(self):
        try:
            import error_handler.notifications.signals  # noqa F401
        except ImportError:
            pass
