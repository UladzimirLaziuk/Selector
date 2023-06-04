from rest_framework import serializers
from selector_app import models
from django.urls import reverse

class SearchModelProcessingSerializer(serializers.ModelSerializer):
    # detail_link = serializers.HyperlinkedIdentityField(
    #     view_name='task_detail',
    #     lookup_field='task_search__id_worker'
    # )
    class Meta:
        model = models.SearchModel
        fields = 'class_name', 'photo_search'#, 'detail_link'
        # extra_kwargs = {'photo_search': {'write_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.task_search.status_search == 'completed':
            representation['result'] = instance.model_search.result_search_images.all()
        else:
            representation['status'] = instance.task_search.status_search
            representation['id_worker'] = instance.task_search.id_worker
            detail_url = reverse('task_detail', args=[instance.task_search.id_worker])
            request = self.context['request']
            representation['detail_link'] = request.build_absolute_uri(detail_url)

        return representation


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskModel
        fields = 'status_search',

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.status_search == 'completed':
            representation['list_images'] = instance.model_search.result_search_model.first().result_search_images.all()
        else:
            pass
            # representation['result'] = 'Processing'
        return representation