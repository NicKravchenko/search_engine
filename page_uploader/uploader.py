"""Page Uploader module."""
import json
from core.models import Page
import zipfile
import os


def processZipFile(file):
    """Processes a zip file."""
    with zipfile.ZipFile(file) as archive:
        for name in archive.namelist():
            file = archive.open(name)
            if file:
                processFile(file)
        return


def saveJsonFile(file):
    """Saves a json file to the database."""

    pages_data = json.loads(file.read())
    upload_pages(pages_data)
    # print(pages_data)


def processFile(file):
    """Processes a file. If it's a .zip file, it will extract it and process"""

    filename = file.name
    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension == ".zip":
        processZipFile(file)

    if file_extension == ".json":
        saveJsonFile(file)
        return


def process_page_data(page, page_data):
    """Processes the page data and returns a dictionary with the data."""

    page.title = page_data["title"]
    page.headers = page_data["headings"]
    page.text = page_data["body"]

    return page


def upload_pages(pages_data):
    """Uploads pages to the database."""

    for url, page_data in pages_data.items():
        try:
            page, created = Page.objects.get_or_create(url=url)

            page = process_page_data(page, page_data)

            if page.title == "No title":
                page.delete()
                print(f"Page was corupted: {url}")
                continue

            page.save()

            if created:
                print(f"Created new page: {url}")
            else:
                print(f"Updated page: {url}")
        except Exception as e:
            print(f"Error uploading page: {url} - {e}")
