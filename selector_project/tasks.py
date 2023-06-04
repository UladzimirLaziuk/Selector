import os.path
import time
import redis
from celery import shared_task
import logging

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from selector_project import settings
from selector_project.celery import app

from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils import timezone
import pytz
from selector_app import models
from selector_app.sim_search_ds import MySearchImage
from selector_project.settings import BASE_DIR

@app.task(name="image_processing_task", bind=True)
def image_processing_task(self, *args, **kwargs):
    print(args, kwargs)
    obj_search = MySearchImage(class_name=kwargs.get('class_name'))
    photo_search = kwargs.get('photo_search')
    model_id = kwargs.get('model_id')
    if obj_search and photo_search:
        photo_search_path = os.path.join(BASE_DIR, photo_search.lstrip('/'))
        print(photo_search_path)
        dict_result = obj_search.get_sorted_similar_images(photo_search_path, 10, show=False)
        print(dict_result)
        model_search = models.SearchModel.objects.get(pk=model_id)
        obj_result = models.ResultSearch.objects.create(model_search=model_search)
        img_result = [models.ImageResultModel(index_photo=index, path_photo=path, model_result_search=obj_result) for
                      index, path in dict_result.items()]

        models.ImageResultModel.objects.bulk_create(img_result)
        model_task = models.TaskModel.objects.filter(id_worker=self.request.id).update(status_search='completed')
        print(model_task)
