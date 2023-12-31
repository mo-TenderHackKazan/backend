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
    queryset = ErrorSummery.objects.filter(parent__isnull=True).prefetch_related("type")


class ListErrorsAPIView(generics.ListAPIView):
    pagination_class = BigResultsSetPagination
    serializer_class = ListErrorsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ErrorFilter

    def get_queryset(self):
        if "reversed" in self.request.GET and self.request.GET["reversed"] == "true":
            return Error.objects.all().reverse()
        return Error.objects.all()


class ListDateErrorsAPIView(generics.ListAPIView):
    serializer_class = ErrorDateAmountSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ErrorDateAmountFilter

    def get_queryset(self):
        if "parent" in self.request.GET:
            return ErrorDateAmount.objects.all()
        return ErrorDateAmount.objects.filter(
            error_id__in=ErrorType.objects.filter(parent_error__isnull=True)
        )

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


class RetrieveErrorTypeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = FullErrorTypeSerializer
    lookup_field = "pk"
    queryset = ErrorType.objects.all()


class CountTodayErrorsAPIView(generics.RetrieveAPIView):
    serializer_class = TodayErrorSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            data={"amount": len(Error.objects.filter(created__date=now().date()))}
        )


class FindErrorsAPIView(generics.ListAPIView):
    pagination_class = BigResultsSetPagination
    serializer_class = ListErrorsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ErrorFilter
    queryset = Error.objects.none()

    def get_queryset(self):
        return Error.objects.filter(
            body__icontains=self.kwargs["search"]
        ) | Error.objects.filter(body__in=self.kwargs["search"])
