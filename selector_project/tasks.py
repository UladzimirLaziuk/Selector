import time


import numpy as np
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
from app_detect import models
from app_detect.detection_utils import predict_model, get_model_stream
from ultralytics.yolo.utils import LOGGER





@app.task(name="rtsp_processing_task", bind=True)
def rtsp_processing_task(self, *args, source=None, save=True, classes=0, line_thickness=1, show=False,
                         project=settings.BASE_DIR, model_id=None, **kwargs):
    pass


