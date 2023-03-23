from rest_framework.serializers import ModelSerializer
from core.models import Page

class PageSerializer(ModelSerializer):

    class Meta:
        model = Page
        fields = ["url", "title", "text"]
