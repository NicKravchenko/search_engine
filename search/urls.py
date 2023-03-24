from django.urls import path
from search.views import SearchListView

urlpatterns = [
    path('', SearchListView.as_view(), name='search-list'),
]
