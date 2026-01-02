from random import randint

import pygame
from pytmx.util_pygame import load_pygame

from ui import UI
from settings import TILE_SIZE
from tile import Tile
from player import Player
from weapon import Weapon
from enemy import Enemy
from praticles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade

# from debug import debug

class Level:
    def __init__(self):
        self.display_surf = pygame.display.get_surface()
        self.game_paused = False

        # sprite groups
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # attack
        self.current_attack = None

        self.create_map()

        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    # noinspection PyAttributeOutsideInit,PyTypeChecker,PyUnresolvedReferences
    def create_map(self):
        map_ = load_pygame('../assets/map/map.tmx')

        for x, y, surf in map_.get_layer_by_name('Grass').tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE),
                 [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                 'grass', surf)

        for x, y, surf in map_.get_layer_by_name('Objects').tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE), [self.visible_sprites, self.obstacle_sprites],
                 'object', surf)

        for x, y, surf in map_.get_layer_by_name('FloorBlocks').tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE), [self.obstacle_sprites], 'invisible')

        for obj in map_.get_layer_by_name('Entity-Pos'):
            if obj.name == "player":
                self.player = Player((obj.x, obj.y), [self.visible_sprites],
                                     self.obstacle_sprites, self.create_attack, self.destroy_attack,
                                     self.create_magic)
            else:
                Enemy(obj.name, (obj.x, obj.y), [self.visible_sprites, self.attackable_sprites],
                      self.obstacle_sprites, self.damage_player, self.trigger_death_particles,
                      self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 70)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:  # enemy
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

            # particles
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.half_width = self.display_surf.get_size()[0] // 2
        self.half_height = self.display_surf.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # floor
        self.floor_surf = pygame.image.load('../assets/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = -(player.rect.centerx - self.half_width)
        self.offset.y = -(player.rect.centery - self.half_height)

        # draw floor
        floor_offset = -(self.floor_rect.topleft - self.offset)
        self.display_surf.blit(self.floor_surf, floor_offset)

        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surf.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type')
                         and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
