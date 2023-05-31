from rest_framework import serializers
from selector_app import models


class SearchModelProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SearchModel
        fields = 'class_name', 'photo_search'
        extra_kwargs = {'__all__': {'write_only': True}}


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.status == 'completed':
            representation['result'] = instance.model_search.result_search_images.all()
        else:
            representation['result'] = 'Processing'
        return representation