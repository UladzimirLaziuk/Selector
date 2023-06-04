import json
import logging
import os
from urllib.parse import urlparse
from django.core.management import call_command
from django.conf import settings
from django.core.management import BaseCommand
import shutil
from DeepImageSearch import Index, LoadData


class Command(BaseCommand):
    help = 'extract'

    def handle(self, *args, **options):

        path_folder_meta = os.path.join(settings.BASE_DIR, 'meta')
        os.makedirs(path_folder_meta, exist_ok=True)
        path_folder = os.path.join(settings.BASE_DIR, 'Selector')
        meta_ds = os.path.join(settings.BASE_DIR, 'meta-data-files')
        for name_folder_source in os.listdir(path_folder):
            name_folder = '_'.join(name_folder_source.split()[:2]) + '_meta'.strip()

            path_dir = os.path.join(path_folder, name_folder_source)
            image_list = LoadData().from_folder([path_dir])
            Index(image_list).Start()


            path_folder_meta_target = os.path.join(path_folder_meta, name_folder)
            if os.path.exists(path_folder_meta_target):
                shutil.rmtree(path_folder_meta_target)
            shutil.move(meta_ds, path_folder_meta_target)

            self.stdout.write(
                self.style.SUCCESS(f'Successfully  {name_folder}'))


