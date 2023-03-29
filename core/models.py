"""Models for the core app."""

from django.db import models
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import (
    GinIndex,
)  # add the Postgres recommended GIN index
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import F
from django.db.models.functions import Concat
from django.db.models import CharField, TextField


class Page(models.Model):
    """Model for a web page."""

    url = models.URLField(unique=True)
    headers = models.TextField()
    title = models.CharField(max_length=255)
    text = models.TextField()
    vector_column = SearchVectorField(null=True)  # new field

    def __str__(self):
        return self.title

    class Meta:
        indexes = (GinIndex(fields=["vector_column"]),)

    def update_search_vector(sender):
        sender.vector_column = SearchVector("title", "text")
        sender.save()
