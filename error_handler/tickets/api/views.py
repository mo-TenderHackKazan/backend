from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from error_handler.tickets.api.serializers import TicketSerializer
from error_handler.tickets.services import get_ticket_data


class RetrieveTicketSerializer(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        data = get_ticket_data(self.kwargs["uuid"])
        return Response(data)
