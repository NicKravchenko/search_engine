from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Page
from search.serializers import PageSerializer
from page_uploader.uploader import upload_pages
import json


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
        file_obj = request.FILES.get("file")
        pages_data = json.loads(file_obj.read())
        if file_obj:
            # print("File uploaded")
            # print(pages_data)
            upload_pages(pages_data)

        return Response({"results": "Pages uploaded"})
