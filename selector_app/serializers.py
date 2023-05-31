from rest_framework import serializers
from selector_app import models


class SearchModelProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SearchModel
        fields = 'class_name', 'photo_search'
        # extra_kwargs = {'photo_search': {'write_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.task_search.status_search == 'completed':
            representation['result'] = instance.model_search.result_search_images.all()
        else:
            representation['status'] = instance.task_search.status_search
            representation['id_worker'] = instance.task_search.id_worker

        return representation


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskModel
        fields = 'status_search',

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.status_search == 'completed':
            representation['result'] = instance.model_search.result_search_images.all()
        else:
            pass
            # representation['result'] = 'Processing'
        return representation