"""Page Uploader module."""
import json
from core.models import Page
import time

def upload_pages(pages_data):
    """Uploads pages to the database."""

    for url, page_data in pages_data.items():
        page, created = Page.objects.get_or_create(url=url)

        page.title = page_data['title']
        page.headers = page_data['headings']
        page.text = page_data['body']

        page.save()

        if created:
            print(f"Created new page: {url}")
        else:
            print(f"Updated page: {url}")
