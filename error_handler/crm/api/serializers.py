from functools import lru_cache

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from error_handler.crm.models import ErrorDateAmount, ErrorSummery
from error_handler.errors.models import Error, ErrorType


class ErrorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorType
        fields = ["id", "name", "resolved", "classes"]


class FullErrorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorType
        fields = ["id", "name", "resolved", "classes"]


class ErrorSerializer(serializers.ModelSerializer):
    type = ErrorTypeSerializer()

    class Meta:
        model = Error
        fields = ["eid", "type", "created", "filtered", "body"]


class ErrorSummerySerializer(serializers.ModelSerializer):
    type = ErrorTypeSerializer()

    class Meta:
        model = ErrorSummery
        fields = ["type", "first_entry", "last_entry", "amount"]


@lru_cache
def get_error_name_by_id(id: int) -> str:
    return ErrorType.objects.get(id=id).name


class ListErrorsSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(method_name="get_type")

    @extend_schema_field(serializers.CharField)
    def get_type(self, obj):
        return get_error_name_by_id(obj.type_id)

    class Meta:
        model = Error
        fields = ["id", "eid", "type", "created", "filtered", "params", "body"]


class ErrorDateAmountSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(method_name="get_type")

    @extend_schema_field(serializers.CharField)
    def get_type(self, obj):
        return get_error_name_by_id(obj.error_id)

    class Meta:
        model = ErrorDateAmount
        fields = ["date", "type", "amount"]


class ResolveErrorNotificationsMethodSerializer(serializers.Serializer):
    options = serializers.ListSerializer(child=serializers.CharField())


class ResolveErrorSerializer(serializers.Serializer):
    options = serializers.ListSerializer(child=serializers.CharField())
    error = serializers.IntegerField()
