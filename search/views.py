"""Search views."""

from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Page
from search.serializers import PageSerializer

from django.db.models.functions import Length


class SearchListView(APIView):
    """Searches the database for pages containing the given query."""

    serializer_class = PageSerializer

    @extend_schema(
        description="Search the database for pages containing the given query",
        parameters=[
            OpenApiParameter(
                name="q", description="Search text", required=True, type=str
            )
        ],
        operation_id="search-get",
        responses={200: PageSerializer(many=True)},
    )
    def get(self, request, format=None):
        """Searches the database for pages containing the given query."""
        query = request.GET.get("q", None)

        if not query:
            return Response({"error": "No query specified"})

        results = processSearch(query)

        return Response({"results": results})


def processSearch(query):
    """Processes the search query and returns the results."""

    pages = (
        Page.objects.filter(
            Q(title__icontains=query)
            | Q(text__icontains=query)
            | Q(headers__icontains=query)
        )
        .annotate(url_length=Length("url"))
        .order_by("url_length")
    )

    results = []
    for page in pages:
        print(page.url)
        results.append({"url": page.url, "title": page.title, "content": page.text})

    return results
