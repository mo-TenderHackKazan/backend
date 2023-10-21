from django.apps import AppConfig


class CrmConfig(AppConfig):
    name = "error_handler.crm"

    def ready(self):
        import error_handler.errors.signals  # noqa
