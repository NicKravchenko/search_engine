"""Models for the core app."""

from django.db import models

class Page(models.Model):
    """Model for a web page."""

    url = models.URLField(unique=True)
    headers = models.TextField()
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title
