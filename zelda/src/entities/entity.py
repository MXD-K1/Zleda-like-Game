import pygame

from src.settings import LAYERS


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups: list[pygame.sprite.Group], image):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()  # Have to be replaced
        self.hitbox = self.rect.copy()
        self.z = LAYERS['main']

        # graphics
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = pygame.sprite.Group()  # Have to be replaced

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self._move_axis(speed, axis="horizontal")
        self._move_axis(speed, axis="vertical")

    def _move_axis(self, speed, axis):
        if axis == "horizontal":
            self.rect.x += self.direction.x * speed
            self.hitbox.centerx = self.rect.centerx
            self._collision(axis)
        elif axis == "vertical":
            self.rect.y += self.direction.y * speed
            self.hitbox.centery = self.rect.centery
            self._collision(axis)

    def _collision(self, axis):
        for sprite in self.obstacle_sprites:
            if not sprite.hitbox.colliderect(self.hitbox):
                continue
            if axis == "horizontal":
                if self.direction.x < 0:  # right
                    self.hitbox.left = sprite.hitbox.right
                if self.direction.x > 0:  # left
                    self.hitbox.right = sprite.hitbox.left
            elif axis == "vertical":
                if self.direction.y < 0:  # down
                    self.hitbox.top = sprite.hitbox.bottom
                if self.direction.y > 0:  # up
                    self.hitbox.bottom = sprite.hitbox.top
