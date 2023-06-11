from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from selector_app.models import SearchModel, TaskModel
from selector_app import serializers
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.renderers import TemplateHTMLRenderer
# Create your views here.

class HomeView(TemplateView):
    template_name = 'selector_app/index_new.html'


class SearchModelCreateView(CreateAPIView):
    model = SearchModel
    serializer_class = serializers.SearchModelProcessingSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['photo_search', 'class_name'],
            properties={
                'photo_search': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    format='binary',
                    description='The image to process'
                ),
                'class_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format='string',
                    description='class name'
                ),
            },
        )
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MyTemplateHTMLRenderer(TemplateHTMLRenderer):
    def get_template_context(self, object_list, renderer_context):
        response = renderer_context['response']
        if response.exception:
            object_list['status_code'] = response.status_code
        return {'object_list': object_list, 'obj_imag':SearchModel.objects.last().photo_search.url}

class TaskDetailAPIView(RetrieveAPIView):
    queryset = TaskModel.objects.all()
    # renderer_classes = [MyTemplateHTMLRenderer]
    # template_name = 'selector_app/my_task_img.html'
    serializer_class = serializers.TaskModelSerializer
    lookup_field = 'id_worker'
