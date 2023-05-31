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






@app.task(name="image_processing_task")
def image_processing_task(*args, **kwargs):
    print(args, kwargs)
    pass







