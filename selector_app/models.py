from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from selector_project.tasks import image_processing_task
import os


def get_choices():
    for name_folder in os.listdir('./Selector'):
        name = ' '.join(name_folder.split()[:2])
        yield (name, name.title())


class SearchModel(models.Model):

    class_name = models.CharField(max_length=50, choices=get_choices())
    photo_search = models.ImageField(upload_to='search_photo')
    date_search = models.DateTimeField(auto_now=True)


class TaskModel(models.Model):
    model_search = models.OneToOneField(SearchModel, on_delete=models.CASCADE, related_name='task_search')
    status_search = models.CharField(max_length=255, default='in processing')
    id_worker = models.CharField(max_length=255, blank=True, null=True)


class ResultSearch(models.Model):
    model_search = models.ForeignKey(SearchModel, on_delete=models.CASCADE, related_name='result_search_model')
    date_result = models.DateTimeField(auto_now=True)


class ImageResultModel(models.Model):
    model_result_search = models.ForeignKey(ResultSearch, on_delete=models.CASCADE, related_name='result_search_images')
    index_photo = models.IntegerField()
    path_photo = models.CharField(max_length=255)


@receiver(post_save, sender=SearchModel)
def search_processing(sender, instance, created, **kwargs):
    if created:
        task_kwargs = {}
        task_kwargs.update({'model_id': instance.pk})
        task_kwargs.update({'photo_search': instance.photo_search.url})
        task_kwargs.update({'class_name': instance.class_name})
        result = image_processing_task.apply_async(kwargs=task_kwargs)
        TaskModel.objects.create(id_worker=result.id, model_search=instance)

# docker run -p 6379:6379 --name redis -d redis redis-server
