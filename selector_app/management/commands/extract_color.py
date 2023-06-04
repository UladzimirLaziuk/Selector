import json
import logging
import os
from urllib.parse import urlparse
from django.core.management import call_command
from django.conf import settings
from django.core.management import BaseCommand
import shutil
from DeepImageSearch import Index, LoadData
import pandas as pd
from tqdm import tqdm
from PIL import Image

from selector_app.utils_ds import find_missing_color, extract_color_rm


def get_feature_colors(image_list):
    features = []
    for img_path in tqdm(image_list):
        # Extract Features
        try:

            color_bg = find_missing_color([img_path])
            feature = extract_color_rm(img_path, num_colors=3, bg=color_bg)
            features.append(feature)
        except:
            features.append(None)
            continue
    return features



def start_feature_extraction_colors(image_list, path_to_save=''):
    image_data = pd.DataFrame()
    image_data['images_paths'] = image_list
    f_data = get_feature_colors(image_list)
    image_data['features'] = f_data
    image_data = image_data.dropna().reset_index(drop=True)
    image_data.to_pickle(path_to_save)
    print(f"Image Meta Information Saved: [{path_to_save}]")
    return image_data

class Command(BaseCommand):
    help = 'extract color'

    def handle(self, *args, **options):

        path_folder_meta = os.path.join(settings.BASE_DIR, 'meta')
        path_folder = os.path.join(settings.BASE_DIR, 'Selector')
        for name_folder_source in os.listdir(path_folder):
            name_folder = '_'.join(name_folder_source.split()[:2]) + '_meta'.strip()
            path_dir = os.path.join(path_folder, name_folder_source)
            image_list = LoadData().from_folder([path_dir])
            path_to_save = os.path.join(path_folder_meta, name_folder, 'image_features_colors_vectors.pkl')
            start_feature_extraction_colors(image_list, path_to_save=path_to_save)

            self.stdout.write(
                self.style.SUCCESS(f'Successfully  {path_to_save}'))

        # if name_folder in ['dress_solemn_meta', 'dress_homemade_meta']:
        #     continue