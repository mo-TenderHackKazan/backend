from django.urls import path

from error_handler.crm.api.views import (
    CountTodayErrorsAPIView,
    FindErrorsAPIView,
    ListDateErrorsAPIView,
    ListErrorResolveNotificationsMethodsAPIView,
    ListErrorsAPIView,
    ListErrorSummeryAPIView,
    ResolveErrorAPIView,
    RetrieveErrorAPIView,
    RetrieveErrorTypeAPIView,
)

app_name = "crm"

urlpatterns = [
    path("errors/types", ListErrorSummeryAPIView.as_view()),
    path("errors/types/<int:pk>", RetrieveErrorTypeAPIView.as_view()),
    path("errors/date", ListDateErrorsAPIView.as_view()),
    path("errors/today", CountTodayErrorsAPIView.as_view()),
    path("errors/", ListErrorsAPIView.as_view()),
    path("errors/search/<str:search>", FindErrorsAPIView.as_view()),
    path("errors/<int:pk>", RetrieveErrorAPIView.as_view()),
    path("resolve/methods", ListErrorResolveNotificationsMethodsAPIView.as_view()),
    path("resolve/", ResolveErrorAPIView.as_view()),
]
