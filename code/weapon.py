import pygame

from support import get_assets_dir


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups: list[pygame.sprite.Group]):
        super().__init__(*groups)
        self.sprite_type = 'weapon'
        self.z = player.z
        direction = player.status.split('_')[0]

        full_path = get_assets_dir() + f'graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midright=player.rect.midleft)
