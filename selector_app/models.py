from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class SearchModel(models.Model):
    class_name = models.CharField(max_length=255)
    photo_search = models.ImageField(upload_to='search_photo')
    date_search = models.DateTimeField(auto_now=True)
    id_worker = models.CharField(max_length=255, blank=True, null=True)
    status_search = models.CharField(max_length=255, default='in processing')


class ResultSearch(models.Model):
    model_search = models.ForeignKey(SearchModel, on_delete=models.CASCADE, related_name='result_search_model')
    date_result = models.DateTimeField(auto_now=True)


class ImageResultModel(models.Model):
    model_result_search = models.ForeignKey(ResultSearch, on_delete=models.CASCADE, related_name='result_search_images')
    photo_search = models.ImageField(upload_to='search_photo')


@receiver(post_save, sender=SearchModel)
def search_processing(sender, instance, created, **kwargs):
    if created:
        pass
