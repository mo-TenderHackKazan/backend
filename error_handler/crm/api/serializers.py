from functools import lru_cache

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from error_handler.crm.models import ErrorDateAmount, ErrorSummery
from error_handler.errors.models import Error, ErrorType


class ErrorTypeSerializer(serializers.ModelSerializer):
    solutions = serializers.SerializerMethodField()

    @extend_schema_field(serializers.IntegerField)
    def get_solutions(self, obj):
        return len(obj.solutions)

    class Meta:
        model = ErrorType
        fields = ["id", "name", "resolved", "solutions", "classes", "has_children"]


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
        fields = [
            "name",
            "type",
            "first_entry",
            "last_entry",
            "last_error_text",
            "amount",
            "children",
        ]


@lru_cache
def get_error_name_by_id(id: int) -> str:
    # e = ErrorType.objects.get(id=id)
    # per = [x.name for x in e.get_parent_list()][::-1] + [e.name]
    # return ". ".join(per)
    return ErrorType.objects.get(id=id).name


@lru_cache
def get_has_children_by_id(id: int) -> str:
    return ErrorType.objects.get(id=id).has_children


class ListErrorsSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(method_name="get_type")

    @extend_schema_field(serializers.CharField)
    def get_type(self, obj):
        return get_error_name_by_id(obj.type_id)

    class Meta:
        model = Error
        fields = ["id", "eid", "type", "created", "filtered", "params", "body"]


class FullErrorTypeSerializer(serializers.ModelSerializer):
    error_description = serializers.CharField(allow_blank=True)
    entries = serializers.SerializerMethodField(read_only=True)
    total = serializers.SerializerMethodField(read_only=True)

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
        fields = [
            "id",
            "total",
            "name",
            "error_description",
            "resolved",
            "solutions",
            "entries",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "total": {"read_only": True},
            "entries": {"read_only": True},
        }


class ErrorDateAmountSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(method_name="get_type")
    has_children = serializers.SerializerMethodField(method_name="get_has_children")

    @extend_schema_field(serializers.CharField)
    def get_type(self, obj):
        return get_error_name_by_id(obj.error_id)

    @extend_schema_field(serializers.BooleanField)
    def get_has_children(self, obj):
        return get_has_children_by_id(obj.error_id)

    class Meta:
        model = ErrorDateAmount
        fields = [
            "error_id",
            "date",
            "type",
            "has_children",
            "amount",
        ]


class ResolveErrorNotificationsMethodSerializer(serializers.Serializer):
    options = serializers.ListSerializer(child=serializers.CharField())


class ResolveErrorSerializer(serializers.Serializer):
    options = serializers.ListSerializer(child=serializers.CharField())
    error = serializers.IntegerField(allow_null=True, required=False)
    body = serializers.CharField()
    email = serializers.EmailField(allow_blank=True, allow_null=True, required=False)


class TodayErrorSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
