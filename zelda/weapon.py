import pygame

from zelda.events import EventBus, Event
from zelda.utils.utils import get_assets_dir
from zelda.settings import LAYERS


class Weapon(pygame.sprite.Sprite):
    def __init__(self, groups: list[pygame.sprite.Group], event_bus: EventBus):
        super().__init__(*groups)
        self.sprite_type = 'weapon'
        self.z = LAYERS['main']
        self.event_bus = event_bus

        direction = self.event_bus.emit(Event.GET_PLAYER_DIRECTION)
        player_weapon = self.event_bus.emit(Event.GET_PLAYER_WEAPON)
        player_rect = self.event_bus.emit(Event.GET_PLAYER_RECT)

        full_path = get_assets_dir() + f'graphics/weapons/{player_weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player_rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player_rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom=player_rect.midtop + pygame.math.Vector2(-10, 0))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player_rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midright=player_rect.midleft)
