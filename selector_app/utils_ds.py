from PIL import Image
from rembg import remove
import colorgram
import numpy as np

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

from itertools import product


def find_missing_color(photo_paths):
    unique_colors = set()

    for photo_path in photo_paths:
        image = Image.open(photo_path)

        image_rgba = image.convert("RGBA")

        pixels = image_rgba.getdata()

        unique_colors.update(set(pixels))

    for r in range(256):
        for g in range(256):
            for b in range(256):
                for a in range(256):
                    color = (r, g, b, a)
                    if color not in unique_colors:
                        return color

    return None


def get_image_remove(path_file=None, color_bg=None):
    cutout = remove(data=Image.open(path_file), bgcolor=color_bg)
    rgb_image = cutout.convert('RGB').resize((500, 500))
    return rgb_image


def remove_closest_color(colors, target_color):
    colors = np.array(colors)
    target_color = np.array(target_color)
    distances = np.linalg.norm(colors - target_color, axis=1)
    closest_index = np.argmin(distances)
    colors = np.delete(colors, closest_index, axis=0)

    return colors


def get_dist(color1, color2):
    color1 = color1 / 255
    color2 = color2 / 255
    color1_rgb = sRGBColor(*color1)
    color2_rgb = sRGBColor(*color2)

    color1_lab = convert_color(color1_rgb, LabColor)

    # Convert from RGB to Lab Color Space
    color2_lab = convert_color(color2_rgb, LabColor)

    # Find the color difference
    delta_e = delta_e_cie2000(color1_lab, color2_lab)
    return delta_e


def get_min_dist(list_q, list_s):
    return [(get_dist(q, s), ind_query, ind_search) for (ind_query, q), (ind_search, s) in
            product(enumerate(list_q), enumerate(list_s))]


def calculate_distance_sum(colors_query, search_colors):
    sum_colors = 0
    while len(colors_query) > 0 and len(search_colors) > 0:
        r = get_min_dist(colors_query, search_colors)
        d, ind_q, ind_s = min(r, key=lambda x: x[0])
        sum_colors += d

        colors_query = list(colors_query.copy())
        colors_query.pop(ind_q)
        search_colors = list(search_colors.copy())
        search_colors.pop(ind_s)
    return sum_colors


def get_new_distance(color, query_color, **kwargs):
    return calculate_distance_sum(search_colors=color, colors_query=query_color)


def sort_colors_by_distance(color_list, query_color, ord=np.inf):
    distances = np.array([get_new_distance(color, query_color, ord=ord) for color in color_list])
    sorted_indices = np.argsort(distances)
    sorted_distances = distances[sorted_indices]
    return sorted_indices, sorted_distances


def extract_color_rm(path_image, num_colors=2, bg=None):
    image = get_image_remove(path_file=path_image, color_bg=bg)
    colors = colorgram.extract(image, num_colors)
    list_colors = []
    for color in colors[:]:
        list_colors.append((color.rgb.r, color.rgb.g, color.rgb.b))
    colors = remove_closest_color(np.array(list_colors), bg[:3])
    return colors
