from os import walk
from os.path import normpath

from pygame.image import load

def import_folder(path):
    surf_list = []
    for _, _, images in walk(path):
        for img in images:
            full_path = path + '/' + img
            image_surf = load(full_path).convert_alpha()
            surf_list.append(image_surf)

    return surf_list

def norm_path(path):
    """Not finished yet"""
    return normpath(path)

def get_assets_dir():
    """Not finished yet"""
    return '../assets/'

__all__ = ['import_folder', 'norm_path', 'get_assets_dir']
