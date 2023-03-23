import json
from search_engine.models import Page

with open('pages.json', 'r') as f:
    pages_data = json.load(f)

for url, page_data in pages_data.items():
    # Create a new Page object and set its fields
    page = Page()
    page.url = url
    page.title = page_data['title']
    page.headers = ', '.join(page_data['headings'])
    page.text = page_data['body']

    # Save the new Page object to the database
    page.save()
