"""Admin configuration for the core app."""

from django.contrib import admin
from core.models import Page

admin.site.register(Page)
