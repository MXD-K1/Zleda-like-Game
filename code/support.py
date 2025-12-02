from csv import reader
from os import walk

from pygame.image import load


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map)
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surf_list = []
    for _, _, images in walk(path):
        for img in images:
            full_path = path + '/' + img
            image_surf = load(full_path).convert_alpha()
            surf_list.append(image_surf)

    return surf_list

__all__ = ['import_folder', 'import_csv_layout']
