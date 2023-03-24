from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Page
from search.serializers import PageSerializer


class UploadView(APIView):
    @extend_schema(
        operation_id="upload_file",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {"file": {"type": "string", "format": "binary"}},
            }
        },
    )
    def put(self, request, format=None):
        file_obj = request.FILES.get('file')
        if (file_obj):
            print("File uploaded")
            print(file_obj.read())

        return Response({"results": "Pages uploaded"})
