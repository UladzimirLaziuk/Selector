from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from selector_project.tasks import image_processing_task

class SearchModel(models.Model):
    class_name = models.CharField(max_length=255)
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
    photo_search = models.ImageField(upload_to='search_photo')


@receiver(post_save, sender=SearchModel)
def search_processing(sender, instance, created, **kwargs):
    if created:
        task_kwargs = {}
        task_kwargs.update({'model_id': instance.pk})
        task_kwargs.update({'photo_search': instance.photo_search.url})
        # result = image_processing_task.apply_async(args=None, kwargs={'id':5})
        result = image_processing_task.delay(**task_kwargs)
