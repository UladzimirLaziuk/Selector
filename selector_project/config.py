import os
from django.conf import settings


def get_image_data_with_features_pkl(class_name:str):
    class_name = '_'.join(class_name.split())
    return os.path.join(settings.BASE_DIR, 'meta', f'{class_name}_meta/','image_data_features.pkl')

def get_image_features_vectors_ann(class_name:str):
    class_name = '_'.join(class_name.split())
    return os.path.join(settings.BASE_DIR, 'meta', f'{class_name}_meta/','image_features_vectors.ann')

def get_colors_data_with_features_pkl(class_name:str):
    class_name = '_'.join(class_name.split())
    return os.path.join(settings.BASE_DIR, 'meta', f'{class_name}_meta/','image_features_colors_vectors.pkl')