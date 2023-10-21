from django.urls import path

from error_handler.tickets.api.views import RetrieveTicketSerializer

urlpatterns = [
    path("<str:uuid>", RetrieveTicketSerializer.as_view(), name="ticket"),
]
