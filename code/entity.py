from math import sin

import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups: list[pygame.sprite.Group]):
        super().__init__(*groups)

        # graphics
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

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

    def wave_value(self):  # get alpha
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
