from rest_framework import generics, status
from rest_framework.response import Response

from error_handler.errors.api.serializers import ReportErrorSerializer
from error_handler.errors.tasks import process_error


class ReportErrorAPIView(generics.GenericAPIView):
    serializer_class = ReportErrorSerializer

    def post(self, request, *args, **kwargs):
        serializer = ReportErrorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        process_error.apply_async(kwargs={"body": data["body"]})
        return Response(status=status.HTTP_201_CREATED)
