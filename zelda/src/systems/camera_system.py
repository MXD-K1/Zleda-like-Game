import logging

import pygame

from src.events import Event, EventBus
from src.settings import LAYERS

logger = logging.getLogger(__name__)


class Camera:
    def __init__(self, drawable_sprites, event_bus: EventBus):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        if self.display_surf is None:
            logger.error("Display surface is not initialized.")
            raise Exception("Display surface is not initialized.")

        self.drawable_sprites = drawable_sprites
        self.event_bus = event_bus
        self.half_width = self.display_surf.get_size()[0] // 2
        self.half_height = self.display_surf.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        # draw order

    def custom_draw(self):
        player_rect = self.event_bus.publish(Event.GET_PLAYER_RECT)
        self.offset.x = -(player_rect.centerx - self.half_width)
        self.offset.y = -(player_rect.centery - self.half_height)

        for layer in LAYERS.values():
            for sprite in sorted(
                self.drawable_sprites.sprites(), key=lambda s: s.rect.centery
            ):
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft + self.offset
                    self.display_surf.blit(sprite.image, offset_pos)

    def update(self):
        self.drawable_sprites.update()

    def enemy_update(self, player):
        enemy_sprites = [
            sprite
            for sprite in self.drawable_sprites.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"
        ]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
