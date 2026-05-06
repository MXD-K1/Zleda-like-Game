import logging

import pygame

from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.events import EventBus
from src.settings import LAYERS

logger = logging.getLogger(__name__)


class Camera:
    def __init__(self, map_info, event_bus: EventBus):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        if self.display_surf is None:
            logger.error("Display surface is not initialized.")
            raise Exception("Display surface is not initialized.")

        self.drawable_sprites = map_info["drawable_sprites"]
        self.event_bus = event_bus
        self.half_width = SCREEN_WIDTH // 2
        self.half_height = SCREEN_HEIGHT // 2
        self.offset = pygame.math.Vector2()

        self.map_width = map_info["width"]
        self.map_height = map_info["height"]
        # draw order

    def custom_draw(self, target):
        cam_x, cam_y = self._get_camera_center(target)
        self.offset.x = -cam_x + self.half_width
        self.offset.y = -cam_y + self.half_height

        for layer in LAYERS.values():
            for sprite in sorted(
                self.drawable_sprites.sprites(), key=lambda s: s.rect.centery
            ):
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft + self.offset
                    self.display_surf.blit(sprite.image, offset_pos)

    def _get_camera_center(self, target):
        min_cam_x = self.half_width
        min_cam_y = self.half_height
        max_cam_x = max(self.half_width, self.map_width - self.half_width)
        max_cam_y = max(self.half_height, self.map_height - self.half_height)

        cam_x = pygame.math.clamp(target.rect.centerx, min_cam_x, max_cam_x)
        cam_y = pygame.math.clamp(target.rect.centery, min_cam_y, max_cam_y)
        return cam_x, cam_y

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
