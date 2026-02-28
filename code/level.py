from random import randint

import pygame

from ui import UI
from settings import LAYERS
from weapon import Weapon
from praticles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from map_loader import MapLoader
from code.utils.utils import get_assets_dir
from events import EventBus, Event
from data.images import load_images

# from debug import debug

class Level:
    def __init__(self):
        images = load_images()

        self.display_surf = pygame.display.get_surface()
        self.event_bus = EventBus()
        self.game_paused = False

        # sprite groups
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # attack
        self.current_attack = None
        self.map_loader = MapLoader(self)
        self.map_loader.load_map(get_assets_dir() + 'map/map.tmx')
        self.player = self.map_loader.player

        self.ui = UI(self.event_bus)
        self.upgrade = Upgrade(self.player)
        self.should_display_start_screen = False

        # particles
        self.animation_player = AnimationPlayer(images)
        self.magic_player = MagicPlayer(self.animation_player)

        # events
        self.subscribe_events()

        # sound
        self.background_sound = pygame.mixer.Sound(get_assets_dir() + 'audio/main.ogg')
        self.background_sound.set_volume(0.5)
        self.background_sound.play(-1)

    def load_game(self):
        pass

    def display_start_screen(self):
        self.display_surf.fill((50, 50, 50))

    def subscribe_events(self):
        self.event_bus.subscribe(Event.CREATE_ATTACK, self.create_attack)
        self.event_bus.subscribe(Event.DESTROY_ATTACK, self.destroy_attack)
        self.event_bus.subscribe(Event.CAST_MAGIC, self.create_magic)
        self.event_bus.subscribe(Event.GET_PLAYER_DIRECTION, self.player.get_direction)
        self.event_bus.subscribe(Event.GET_PLAYER_RECT, self.player.get_rect)
        self.event_bus.subscribe(Event.GET_PLAYER_WEAPON, self.player.get_weapon)
        self.event_bus.subscribe(Event.GET_PLAYER_EXP, self.player.get_exp)
        self.event_bus.subscribe(Event.GET_PLAYER_HEALTH, self.player.get_health)
        self.event_bus.subscribe(Event.GET_PLAYER_ENERGY, self.player.get_energy)
        self.event_bus.subscribe(Event.GET_PLAYER_STATS, self.player.get_stats)

    def create_attack(self):
        self.current_attack = Weapon([self.visible_sprites, self.attack_sprites], self.event_bus)

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
        if not self.should_display_start_screen:
            self.visible_sprites.custom_draw(self.player)
            self.ui.display(self.player)

            if self.game_paused:
                self.upgrade.display()
            else:
                self.visible_sprites.update()
                self.visible_sprites.enemy_update(self.player)
                self.player_attack_logic()
        else:
            self.background_sound.stop()  # make sure it plays again when the game loads
            self.display_start_screen()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.half_width = self.display_surf.get_size()[0] // 2
        self.half_height = self.display_surf.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        # draw order

    def custom_draw(self, player):
        self.offset.x = -(player.rect.centerx - self.half_width)
        self.offset.y = -(player.rect.centery - self.half_height)

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft + self.offset
                    self.display_surf.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type')
                         and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
