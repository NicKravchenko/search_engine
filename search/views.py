"""Search views."""

from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer

from django.db.models import F
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Page
from search.serializers import PageSerializer

from django.contrib.postgres.search import SearchQuery, SearchRank


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
        responses={
            200: inline_serializer(
                name='CustomResponse',
                fields={
                    'results': serializers.ListField(
                        child=inline_serializer(
                            name='ResultItem',
                            fields={
                                'url': serializers.URLField(),
                                'title': serializers.CharField(),
                                'content': serializers.CharField(),
                            }
                        )
                    )
                }
            )
        },
    )
    def get(self, request, format=None):
        """Searches the database for pages containing the given query."""
        query = request.GET.get("q", None)

        if not query:
            return Response({"error": "No query specified"})

        pages = processSearch(query)
        print(pages)
        # results = PageResultSerializer(pages, many=True)
        results = pages
        return Response({"results": results})


def processSearch(query):
    """Processes the search query and returns the results."""

    search_query = SearchQuery(query)
    rank_annotation = SearchRank(F("vector_column"), search_query)

    pages = (
        Page.objects.annotate(
            rank=rank_annotation,
        )
        .filter(vector_column=search_query)
        .order_by("-rank")
        .distinct()[:40]
    )

    results = getPages(pages)

    return results


def getPages(pages):
    results = []
    for page in pages:
        print(page.url)
        results.append(
            {"url": page.url, "title": page.title, "content": page.text[:2000]}
        )
    return results
