import os
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Page
from page_uploader.uploader import processFile




class UploadView(APIView):
    """Uploads pages to the database."""

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "description": "Files to upload. .zip for archives, .json for single files",
                        "items": {
                            "type": "string",
                            "format": "binary"
                        }
                    }
                },
            },
        },
    )
    def put(self, request, format=None):
        """Uploads pages to the database."""
        try:
            for file in request.FILES.getlist('files'):
                processFile(file)

            return Response({"message": "Files uploaded successfully"})
        except Exception as e:
            print(e)
            return Response({"error": str(e)})
