from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Page


@extend_schema(
    description="Search the database for pages containing the given query",
    parameters=[
        OpenApiParameter(
            name="artist", description="Filter by artist", required=False, type=str
        ),
        OpenApiParameter(
            name="release",
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            description="Filter by release date",
            examples=[
                OpenApiExample(
                    "Example 1",
                    summary="short optional summary",
                    description="longer description",
                    value="1993-08-23",
                ),
            ],
        ),
    ],
    responses={
        "200": {
            "description": "Search results",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "results": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "url": {"type": "string"},
                                        "title": {"type": "string"},
                                        "content": {"type": "string"},
                                    },
                                },
                            }
                        },
                    }
                }
            },
        }
    },
)
@api_view(["GET"])
def search(request):
    query = request.GET.get("q")
    if not query:
        return Response({"error": "No query specified"})

    print(query)

    pages = Page.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))

    results = []
    for page in pages:
        results.append({"url": page.url, "title": page.title, "content": page.text})

    return Response({"results": results})
