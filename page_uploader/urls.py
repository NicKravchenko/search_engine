from django.urls import path
from page_uploader.views import UploadView

urlpatterns = [
    path('', UploadView.as_view(), name='search-list'),
]
