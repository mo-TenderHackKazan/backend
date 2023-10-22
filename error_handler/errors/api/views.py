import requests
from rest_framework import generics
from rest_framework.response import Response

from error_handler.errors.api.serializers import ReportErrorSerializer
from error_handler.errors.tasks import ML_HOST, process_error


class ReportErrorAPIView(generics.GenericAPIView):
    serializer_class = ReportErrorSerializer

    def post(self, request, *args, **kwargs):
        serializer = ReportErrorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        process_error.apply_async(kwargs={"body": data["body"]})
        res = requests.post(ML_HOST + "error", json={"log": data["body"]})
        return Response(data=res.json())
