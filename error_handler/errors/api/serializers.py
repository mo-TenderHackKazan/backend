from rest_framework import serializers


class ReportErrorSerializer(serializers.Serializer):
    occurred = serializers.DateTimeField(allow_null=True, required=False)
    body = serializers.CharField()
    source = serializers.CharField(allow_null=True, allow_blank=True, required=False)
