from functools import lru_cache

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from error_handler.crm.models import ErrorDateAmount, ErrorSummery
from error_handler.errors.models import Error, ErrorType


class ErrorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorType
        fields = ["id", "name", "resolved", "classes", "has_children"]


class ErrorSerializer(serializers.ModelSerializer):
    type = ErrorTypeSerializer()

    class Meta:
        model = Error
        fields = ["eid", "type", "created", "filtered", "body"]


class ErrorSummerySerializer(serializers.ModelSerializer):
    type = ErrorTypeSerializer()
    children = serializers.SerializerMethodField()
    name = serializers.CharField(source="type.name")

    @extend_schema_field(serializers.ListSerializer(child=serializers.JSONField()))
    def get_children(self, obj):
        if obj.children is not None:
            return ErrorSummerySerializer(many=True).to_representation(obj.children)
        else:
            return None

    class Meta:
        model = ErrorSummery
        fields = ["name", "type", "first_entry", "last_entry", "amount", "children"]


@lru_cache
def get_error_name_by_id(id: int) -> str:
    e = ErrorType.objects.get(id=id)
    per = [x.name for x in e.get_parent_list()][::-1] + [e.name]
    return ". ".join(per)


class ListErrorsSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(method_name="get_type")

    @extend_schema_field(serializers.CharField)
    def get_type(self, obj):
        return get_error_name_by_id(obj.type_id)

    class Meta:
        model = Error
        fields = ["id", "eid", "type", "created", "filtered", "params", "body"]


class FullErrorTypeSerializer(serializers.ModelSerializer):
    entries = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    @extend_schema_field(serializers.IntegerField)
    def get_total(self, obj):
        return len(obj.entries.all())

    @extend_schema_field(ListErrorsSerializer(many=True))
    def get_entries(self, obj):
        return ListErrorsSerializer(many=True).to_representation(
            obj.entries.all()[:100]
        )

    class Meta:
        model = ErrorType
        fields = ["id", "total", "name", "resolved", "classes", "solutions", "entries"]


class ErrorDateAmountSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(method_name="get_type")

    @extend_schema_field(serializers.CharField)
    def get_type(self, obj):
        return get_error_name_by_id(obj.error_id)

    class Meta:
        model = ErrorDateAmount
        fields = ["error_id", "date", "type", "amount"]


class ResolveErrorNotificationsMethodSerializer(serializers.Serializer):
    options = serializers.ListSerializer(child=serializers.CharField())


class ResolveErrorSerializer(serializers.Serializer):
    options = serializers.ListSerializer(child=serializers.CharField())
    error = serializers.IntegerField()
    body = serializers.CharField()
    email = serializers.EmailField(allow_blank=True, allow_null=True, required=False)


class TodayErrorSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
