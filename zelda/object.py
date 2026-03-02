import pygame

from zelda.settings import LAYERS
from zelda.tile import Tile

class Object(Tile):
    def __init__(self, pos, groups: list[pygame.sprite.Group], sprite_type, surface):
        super().__init__(pos, groups, sprite_type, surface)
        self.z = LAYERS['main']
