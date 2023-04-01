"""Serializers for the search app."""

from rest_framework.serializers import ModelSerializer
from core.models import Page


class PageSerializer(ModelSerializer):
    """Serializer for the Page model."""

    class Meta:
        model = Page
        fields = "__all__"

