"""Models for the core app."""

from django.db import models
from django.contrib.postgres.search import SearchVectorField


class Page(models.Model):
    """Model for a web page."""

    url = models.URLField(unique=True)
    headers = models.TextField()
    title = models.CharField(max_length=255)
    text = models.TextField()

    # search_vector = SearchVectorField(null=True)

    def __str__(self):
        return self.title
