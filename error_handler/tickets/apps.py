from django.apps import AppConfig


class TicketsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "error_handler.tickets"

    def ready(self):
        try:
            import error_handler.tickets.signals  # noqa F401
        except ImportError:
            pass
