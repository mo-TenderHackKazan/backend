from django.urls import path

from error_handler.errors.api.views import ReportErrorAPIView

app_name = "errors"

urlpatterns = [
    path("report", ReportErrorAPIView.as_view()),
]
