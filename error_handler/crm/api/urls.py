from django.urls import path

from error_handler.crm.api.views import (
    ListDateErrorsAPIView,
    ListErrorResolveNotificationsMethodsAPIView,
    ListErrorsAPIView,
    ListErrorSummeryAPIView,
    ResolveErrorAPIView,
    RetrieveErrorAPIView,
)

app_name = "crm"

urlpatterns = [
    path("errors/types", ListErrorSummeryAPIView.as_view()),
    path("errors/date", ListDateErrorsAPIView.as_view()),
    path("errors/", ListErrorsAPIView.as_view()),
    path("errors/<int:pk>", RetrieveErrorAPIView.as_view()),
    path("resolve/methods", ListErrorResolveNotificationsMethodsAPIView.as_view()),
    path("resolve/", ResolveErrorAPIView.as_view()),
]
