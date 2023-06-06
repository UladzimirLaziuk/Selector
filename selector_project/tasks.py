import os.path
import time
import redis
from celery import shared_task
import logging

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from selector_app.sim_search_vae import SelectorClass
from selector_project import settings
from selector_project.celery import app


from selector_app import models
from selector_app.sim_search_ds import MySearchImage
from selector_project.settings import BASE_DIR

@app.task(name="image_processing_task_v1", bind=True)
def image_processing_task_v1(self, *args, **kwargs):
    print(args, kwargs)
    obj_search = MySearchImage(class_name=kwargs.get('class_name'))
    photo_search = kwargs.get('photo_search')
    model_id = kwargs.get('model_id')
    if obj_search and photo_search:
        photo_search_path = os.path.join(BASE_DIR, photo_search.lstrip('/'))
        print(photo_search_path)
        dict_result = obj_search.get_sorted_similar_images(photo_search_path, 15, show=False)
        print(dict_result)
        model_search = models.SearchModel.objects.get(pk=model_id)
        obj_result = models.ResultSearch.objects.create(model_search=model_search)
        img_result = [models.ImageResultModel(index_photo=index, path_photo=path, model_result_search=obj_result) for
                      index, path in dict_result.items()]

        models.ImageResultModel.objects.bulk_create(img_result)
        model_task = models.TaskModel.objects.filter(id_worker=self.request.id).update(status_search='completed')
        print(model_task)


@app.task(name="image_processing_task_v2", bind=True)
def image_processing_task_v2(self, *args, **kwargs):
    print(args, kwargs)
    photo_search = kwargs.get('photo_search')
    data_dir = os.path.join(settings.BASE_DIR, 'selector_images')
    obj_selector = SelectorClass(data_dir=data_dir,
                                 color_dir=os.path.join(settings.BASE_DIR,'color_dir'))


    model_id = kwargs.get('model_id')
    if photo_search:
        photo_search_path = os.path.join(BASE_DIR, photo_search.lstrip('/'))
        result_tuple = obj_selector.find_impresses(image_file=photo_search_path, img_category_name=kwargs.get('class_name'))

        # print(result_tuple)
        model_search = models.SearchModel.objects.get(pk=model_id)
        obj_result = models.ResultSearch.objects.create(model_search=model_search)
        img_result = [models.ImageResultModel(index_photo=0, path_photo=os.path.join(data_dir, dt[0]), model_result_search=obj_result) for
                      dt in result_tuple]

        models.ImageResultModel.objects.bulk_create(img_result)
        model_task = models.TaskModel.objects.filter(id_worker=self.request.id).update(status_search='completed')
        print(model_task)


