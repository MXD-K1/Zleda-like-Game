from os import walk
from os.path import normpath

from pygame.transform import flip
from pygame.image import load

def import_folder(path):
    surf_list = []
    for _, _, images in walk(path):
        for img in images:
            full_path = path + '/' + img
            image_surf = load(full_path).convert_alpha()
            surf_list.append(image_surf)

    return surf_list

def import_folder_dict(path):
    surf_dict = {}
    for img_name, _, images in walk(path):
        for img in images:
            full_path = path + '/' + img
            image_surf = load(full_path).convert_alpha()
            surf_dict[img.split('.')[0]] = image_surf

    return surf_dict

def import_folders_of_folder_dict(path):
    surf_dict = {}
    for file_name, _, _ in walk(path, False):

        full_path = path + '/' + file_name.split('\\')[-1]
        surf_dict[file_name.split('\\')[-1]] = import_folder_dict(full_path)

    return surf_dict

def reflect_images(frames):
    new_frames = []
    for frame in frames:
        flipped_frame = flip(frame, True, False)
        new_frames.append(flipped_frame)
    return new_frames

def norm_path(path):
    """Not finished yet"""
    return normpath(path)

def get_assets_dir():
    """Not finished yet"""
    return 'assets/'

__all__ = ['import_folder', 'import_folder_dict', 'import_folders_of_folder_dict', 'norm_path', 'get_assets_dir',
           'reflect_images']
