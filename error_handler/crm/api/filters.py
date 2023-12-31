from django_filters import rest_framework as filters

from error_handler.crm.models import ErrorDateAmount
from error_handler.errors.models import Error


class ErrorFilter(filters.FilterSet):
    date_range = filters.DateTimeFromToRangeFilter(field_name="created")
    date_created = filters.DateFilter(field_name="created__date")
    parent = filters.NumberFilter(field_name="type__parent_error_id")

    class Meta:
        model = Error
        fields = ["date_range", "date_created", "parent", "type"]


class ErrorDateAmountFilter(filters.FilterSet):
    date_range = filters.DateTimeFromToRangeFilter(field_name="date")
    parent = filters.NumberFilter(field_name="error__parent_error_id")

    class Meta:
        model = ErrorDateAmount
        fields = ["date_range", "date", "error", "parent"]
