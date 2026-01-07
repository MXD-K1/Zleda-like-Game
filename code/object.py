import pygame

from settings import LAYERS
from tile import Tile

class Object(Tile):
    def __init__(self, pos, groups: list[pygame.sprite.Group], sprite_type, surface):
        super().__init__(pos, groups, sprite_type, surface)
        self.z = LAYERS['main']
