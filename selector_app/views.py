from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.generics import CreateAPIView

from selector_app.models import SearchModel
from selector_app import serializers

# Create your views here.

class HomeView(TemplateView):
    template_name = 'selector_app/index.html'

class SearchModelCreateView(CreateAPIView):
    model = SearchModel
    serializer_class = serializers.SearchModelProcessingSerializer