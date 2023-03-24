"""Page Uploader module."""
import json
from core.models import Page

def upload_pages(pages_data):
    """Uploads pages to the database."""

    for url, page_data in pages_data.items():
        # Create a new Page object and set its fields
        page = Page()
        page.url = url
        page.title = page_data['title']
        page.headers = ', '.join(page_data['headings'])
        page.text = page_data['body']

        # Save the new Page object to the database
        page.save()
