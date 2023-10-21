from rest_framework import serializers

from error_handler.tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    current = serializers.IntegerField()

    class Meta:
        model = Ticket
        fields = ["name", "current", "max", "next"]
