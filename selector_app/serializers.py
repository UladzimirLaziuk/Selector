from rest_framework import serializers
from selector_app import models


class SearchModelProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SearchModel
        fields = 'class_name', 'photo_search'
        extra_kwargs = {'__all__': {'write_only': True}}


