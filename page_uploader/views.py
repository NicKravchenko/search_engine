"""Views for the page_uploader app."""
from search.serializers import PageSerializer

from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from page_uploader.uploader import processFile


class UploadView(APIView):
    """Uploads pages to the database."""

    serializer_class = PageSerializer

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "description": "Files to upload: .zip for archives, "
                        + ".json for single files. .zip files can contain"
                        + ".json files or other .zip files.",
                        "items": {"type": "string", "format": "binary"},
                    }
                },
            },
        },
    )
    def put(self, request, format=None):
        """Uploads pages to the database."""
        try:
            for file in request.FILES.getlist("files"):
                processFile(file)

            return Response({"message": "Files uploaded successfully"})
        except Exception as e:
            print(e)
            return Response({"error": str(e)})
