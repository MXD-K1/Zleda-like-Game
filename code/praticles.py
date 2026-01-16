from random import choice

import pygame

from settings import LAYERS

class AnimationPlayer:
    def __init__(self, images):
        self.frames = {
            'flame': images['flame'],
            'aura': images['aura'],
            'heal': images['heal'],

            # attacks
            'claw': images['claw'],
            'slash': images['slash'],
            'sparkle': images['sparkle'],
            'leaf_attack': images['leaf_attack'],
            'thunder': images['thunder'],

            # monster deaths
            'squid': images['squid'],
            'raccoon': images['raccoon'],
            'spirit': images['spirit'],
            'bamboo': images['bamboo'],

            # leafs
            'leaf': images['leaf']
        }

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        ParticleEffect(pos, self.frames[animation_type], groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups: list[pygame.sprite.Group]):
        super().__init__(*groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.sprite_type = 'magic'
        self.z = LAYERS['main']

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
