import pygame

from settings import SCALE_FACTOR


def import_image(image_path):
    return pygame.image.load(image_path).convert_alpha()


def cut_spritesheet(spritesheet, cols, rows):
    spritesheet = import_image(spritesheet)
    frames = {}

    cell_width = spritesheet.get_width() / cols
    cell_height = spritesheet.get_height() / rows

    for col in range(cols):
        for row in range(rows):
            surf = spritesheet.subsurface((col * cell_width, row * cell_height, cell_width, cell_height)).copy()
            surf = pygame.transform.scale(surf, (surf.get_width() * SCALE_FACTOR, surf.get_height() * SCALE_FACTOR)).copy()
            frames[(row, col)] = surf
    return frames
