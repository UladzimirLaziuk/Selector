from __future__ import absolute_import
import os
from celery import Celery

# from django.conf import settings
# import django
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selector_project.settings')
# django.setup()

app = Celery('selector_project')
#celery -A Yolov8API worker -l info
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
