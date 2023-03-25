"""Page Uploader module."""
import json
from core.models import Page
import time
import zipfile
import os


def saveJsonFile(file):
    pages_data = json.loads(file.read())
    # upload_pages(pages_data)
    print("------------------------New File------------------------")
    print(pages_data)

def processFile(file):
    filename = file.name
    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension == '.zip':
        with zipfile.ZipFile(file) as archive:
            for name in archive.namelist():
                file = archive.open(name)

                if file:
                    processFile(file)

            return

    if file_extension == '.json':
        saveJsonFile(file)
        return

def upload_pages(pages_data):
    """Uploads pages to the database."""

    for url, page_data in pages_data.items():
        try:
            page, created = Page.objects.get_or_create(url=url)

            page.title = page_data['title']
            page.headers = page_data['headings']
            page.text = page_data['body']

            if page.title == "No title":
                page.delete()
                continue

            page.save()

            if created:
                print(f"Created new page: {url}")
            else:
                print(f"Updated page: {url}")
        except Exception as e:
            print(f"Error uploading page: {url} - {e}")
