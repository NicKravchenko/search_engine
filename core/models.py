"""Models for the core app."""

from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex # add the Postgres recommended GIN index


class Page(models.Model):
    """Model for a web page."""

    url = models.URLField(unique=True)
    headers = models.TextField()
    title = models.CharField(max_length=255)
    text = models.TextField()
    vector_column = SearchVectorField(null=True)  # new field

    # search_vector = SearchVectorField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            # models.Index(fields=['title']),
            # models.Index(fields=['headers']),
            # models.Index(fields=['text']),
            GinIndex(fields=['vector_column']),
        ]
