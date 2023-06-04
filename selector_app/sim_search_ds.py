# from colorthief import ColorThief
import os.path

from DeepImageSearch import SearchImage
from annoy import AnnoyIndex
from PIL import Image, ImageDraw
import pandas as pd
import matplotlib.pyplot as plt

from selector_project import config
from selector_app.utils_ds import extract_color_rm, find_missing_color, sort_colors_by_distance


class MySearchImage(SearchImage):
    def __init__(self, class_name: str):
        meta_images = config.get_image_data_with_features_pkl(class_name)
        self.image_data = pd.read_pickle(meta_images)
        self.meta_vectors_ann = config.get_image_features_vectors_ann(class_name)
        self.meta_vectors_colors = config.get_colors_data_with_features_pkl(class_name)
        if os.path.isfile(self.meta_vectors_colors):
            self.df_colors = pd.read_pickle(self.meta_vectors_colors)
        else:
            self.df_colors = pd.DataFrame()

        # self.image_data = pd.read_pickle(config.image_data_with_features_pkl)
        self.f = len(self.image_data['features'][0])

    def search_by_vector(self, v, n: int):
        self.v = v  # Feature Vector
        self.n = n  # number of output
        u = AnnoyIndex(self.f, 'euclidean')
        u.load(self.meta_vectors_ann)  # super fast, will just mmap the file
        index_list = u.get_nns_by_vector(self.v, self.n)  # will find the 10 nearest neighbors
        return dict(zip(index_list, self.image_data.iloc[index_list]['images_paths'].to_list()))

    def get_sorted_similar_images(self, *args, show=False, threshold_distance=55, **kwargs):
        parent_dict_result = self.get_similar_images(*args, **kwargs)
        if self.df_colors.empty:
            list_full_image = list(parent_dict_result.copy().values())
            list_full_image.append(self.image_path)
            color_bg = find_missing_color(list_full_image)
            query_vector = extract_color_rm(self.image_path, num_colors=3, bg=color_bg)

            color_list = [extract_color_rm(path, num_colors=3, bg=color_bg) for path in parent_dict_result.values()]

        else:
            color_list = self.df_colors.features.loc[parent_dict_result.keys()].tolist()

            color_bg = find_missing_color([self.image_path])
            query_vector = extract_color_rm(self.image_path, num_colors=3, bg=color_bg)


        sorted_indices, sorted_distances = sort_colors_by_distance(color_list, query_vector, ord=1)


        array_sort_colors = []
        for index, dist in zip(sorted_indices, sorted_distances):
            if dist > threshold_distance:
                break
            array_sort_colors.append(list(color_list)[index])

        sorted_dict = {}

        for index, dist in zip(sorted_indices, sorted_distances):
            if dist > threshold_distance:
                break
            key = list(parent_dict_result)[index]
            sorted_dict[key] = parent_dict_result[key]
        if show:
            print('*' * 100)
            print('DeepImageSearch')
            self.display_images_path(parent_dict_result.values(), color_list)
            print('*' * 100)
            print('Sort')
            self.display_images_path(sorted_dict.values(), array_sort_colors)
        return sorted_dict

    @staticmethod
    def display_images_path(image_paths_list, colors=None):
        num_images = len(image_paths_list)

        fig, axes = plt.subplots(nrows=1, ncols=num_images, figsize=(100, 10))
        if num_images == 1:
            axes = [axes]

        for ax, path, color_array in zip(axes, image_paths_list, colors):
            # загрузка изображения
            img = Image.open(path)
            img = img.resize((500, 500))
            width, height = img.size

            # создание изображения для цветов
            color_image = Image.new('RGB', (500, height), (255, 255, 255))
            draw = ImageDraw.Draw(color_image)

            # добавление цветов на изображение

            y = 0
            for color in color_array.reshape(-1, 3):
                draw.rectangle((0, y, 100, y + 20), outline='red', fill=tuple(color.tolist()))
                y += 25

            # объединение двух изображений
            result = Image.new('RGB', (width + 100, height), (255, 255, 255))
            result.paste(img, (0, 0))
            result.paste(color_image, (width, 0))

            # отображение изображения
            ax.imshow(result)
            ax.axis('off')

        plt.show()