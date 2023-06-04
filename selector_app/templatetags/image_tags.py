from django import template
from django.http import HttpRequest
import os
from django.conf import settings

register = template.Library()


@register.filter(name="relative_path")
def relative_path(value):
    relative_path = os.path.relpath(value, os.getcwd())
    return '/' + relative_path
