from math import sin

import pygame

from settings import LAYERS


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

        self.rect.x += self.direction.x * speed
        self.hitbox.centerx = self.rect.centerx
        self.collision('horizontal')

        self.rect.y += self.direction.y * speed
        self.hitbox.centery = self.rect.centery
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x < 0:  # right
                        self.hitbox.left = sprite.hitbox.right
                    if self.direction.x > 0:  # left
                        self.hitbox.right = sprite.hitbox.left

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:  # down
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # up
                        self.hitbox.bottom = sprite.hitbox.top

    @staticmethod
    def wave_value():  # get alpha
        value = sin(pygame.time.get_ticks())
        return 255 if value >= 0 else 0
