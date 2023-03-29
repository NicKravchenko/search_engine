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


from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def processSearch(query):
    """Processes the search query and returns the results."""
    # search_vector = SearchVector("title", "text")
    search_vector = (
        SearchVector("headers", weight="B")
        + SearchVector("title", weight="A")
        + SearchVector("text", weight="C")
    )

    search_query = SearchQuery(query)

    pages = (
        Page.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query),
        )
        .filter(search=search_query)
        .order_by("-rank")
        .distinct()[:5]
    )

    results = []
    for page in pages:
        print(page.url)
        print(page.vector_column)
        results.append({"url": page.url, "title": page.title, "content": page.text})

    return results
