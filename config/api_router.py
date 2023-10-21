from django.urls import include, path

app_name = "api"
urlpatterns = [
    path("ticket/", include("error_handler.tickets.api.urls")),
    path("crm/", include("error_handler.crm.api.urls")),
    path("errors/", include("error_handler.errors.api.urls")),
]
