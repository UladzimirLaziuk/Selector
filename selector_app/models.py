from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from selector_project.tasks import image_processing_task_v1, image_processing_task_v2
import os
from django.conf import settings

def get_choices():
    for name_folder in os.listdir(os.path.join(settings.BASE_DIR, 'Selector')):
        name = ' '.join(name_folder.split()[:2])
        yield (name, name.title())


class SearchModel(models.Model):
    CHOICES_VERSION = (
        ('1', '1 color'),
        ('2', '2 color'),
    )

    version_search = models.CharField(max_length=10, choices=CHOICES_VERSION)
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
        version_search = instance.version_search
        # print(instance.class_name, 'instance.class_name')
        if version_search == '1':
            result = image_processing_task_v1.apply_async(kwargs=task_kwargs)
        else:
            result = image_processing_task_v2.apply_async(kwargs=task_kwargs)
        TaskModel.objects.create(id_worker=result.id, model_search=instance)

# docker run -p 6379:6379 --name redis -d redis redis-server
#sudo apt-get install python3-dev build-essential gcc libpq-dev
