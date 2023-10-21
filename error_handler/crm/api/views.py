from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from error_handler.common.api import BigResultsSetPagination
from error_handler.crm.api.filters import ErrorDateAmountFilter, ErrorFilter
from error_handler.crm.api.serializers import (
    ErrorDateAmountSerializer,
    ErrorSerializer,
    ErrorSummerySerializer,
    FullErrorTypeSerializer,
    ListErrorsSerializer,
    ResolveErrorNotificationsMethodSerializer,
    ResolveErrorSerializer,
    TodayErrorSerializer,
)
from error_handler.crm.models import ErrorDateAmount, ErrorSummery
from error_handler.errors.models import Error, ErrorType
from error_handler.notifications.models import Notification
from error_handler.notifications.services import send_notification


class ListErrorSummeryAPIView(generics.ListAPIView):
    serializer_class = ErrorSummerySerializer
    queryset = ErrorSummery.objects.all().prefetch_related("type")


class ListErrorsAPIView(generics.ListAPIView):
    pagination_class = BigResultsSetPagination
    serializer_class = ListErrorsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ErrorFilter
    queryset = Error.objects.all()


class ListDateErrorsAPIView(generics.ListAPIView):
    serializer_class = ErrorDateAmountSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ErrorDateAmountFilter
    queryset = ErrorDateAmount.objects.all()


class ListErrorResolveNotificationsMethodsAPIView(generics.GenericAPIView):
    serializer_class = ResolveErrorNotificationsMethodSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            data={"options": [y for x, y in Notification.NotificationProviders.choices]}
        )


choices = [y for x, y in Notification.NotificationProviders.choices]


class ResolveErrorAPIView(generics.GenericAPIView):
    serializer_class = ResolveErrorSerializer

    def post(self, request, *args, **kwargs):
        serializer = ResolveErrorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        error = get_object_or_404(ErrorType, id=data["error"])
        if error.resolved:
            raise ValidationError("Error already resolved")
        if any([x not in choices for x in data["options"]]):
            raise ValidationError("Incorrect options")
        for option in set(data["options"]):
            if option == "email":
                send_notification(
                    f"Решение ошибки {error.name}",
                    data["body"],
                    option,
                    email=data["email"],
                )
            else:
                send_notification(f"Решение ошибки {error.name}", data["body"], option)

        return Response(status=status.HTTP_204_NO_CONTENT)


class RetrieveErrorAPIView(generics.RetrieveAPIView):
    serializer_class = ErrorSerializer
    lookup_field = "pk"
    queryset = Error.objects.all()


class RetrieveErrorTypeAPIView(generics.RetrieveAPIView):
    serializer_class = FullErrorTypeSerializer
    lookup_field = "pk"
    queryset = ErrorType.objects.all()


class CountTodayErrorsAPIView(generics.RetrieveAPIView):
    serializer_class = TodayErrorSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            data={"amount": len(Error.objects.filter(created__date=now().date()))}
        )
