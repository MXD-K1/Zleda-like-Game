import sys
import logging
from random import randint

import pygame

from src.ui import UI
from src.settings import LAYERS
from src.weapon import Weapon
from src.particles import AnimationPlayer
from src.magic import MagicPlayer
from src.upgrade import Upgrade
from src.map_loader import MapLoader
from src.utils.utils import get_assets_dir
from src.events import EventBus, Event
from src.data.images import load_images
from src.data.sounds import load_sounds, sounds
from src.data.fonts import init_fonts

# from src.debug import debug

logger = logging.getLogger(__name__)

class Level:
    def __init__(self):
        self.load_game()

        self.display_surf = pygame.display.get_surface()
        self.event_bus = EventBus()
        self.game_paused = False

        # sprite groups
        self.visible_sprites = CameraGroup(self.event_bus)
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # attack
        self.current_attack = None
        self.map_loader = MapLoader(self)
        self.player = self._load_map('map.tmx')

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        # events
        self.subscribe_events()

        self.ui = UI(self.event_bus)
        self.upgrade = Upgrade(self.event_bus)
        self.should_display_start_screen = False

        # sound
        self.background_sound = sounds['background']
        self.background_sound.set_volume(0.5)
        self.background_sound.play(-1)

    @staticmethod
    def load_game():
        def _load_resource(action, label):
            try:
                action()
            except pygame.error as e:
                logger.error(f'Could not load {label}. Error: {e}')
                pygame.quit()
                sys.exit()
            else:
                logger.info(f'Loaded {label} successfully')

        _load_resource(load_images, 'images')
        _load_resource(load_sounds, 'sounds')
        _load_resource(init_fonts, 'fonts')

    def display_start_screen(self):
        self.display_surf.fill((50, 50, 50))

    def _load_map(self, map_name):
        try:
            player = self.map_loader.load_map(get_assets_dir() + f'map/{map_name}')
            return player
        except pygame.error:
            logger.error(f'Could not load map. Error: {pygame.error}')
            pygame.quit()
            sys.exit()

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
        self.event_bus.subscribe(Event.GET_PLAYER_ATTACK_INFO, self.player.get_attack_info)
        self.event_bus.subscribe(Event.ADD_EXP, self.player.add_exp)

    def create_attack(self):
        self.current_attack = Weapon([self.visible_sprites, self.attack_sprites], self.event_bus)

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        elif style == 'flame':
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
                            for _ in range(randint(3, 6)):
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
        self.event_bus.publish(Event.ADD_EXP, amount=amount)
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def _run_active(self):
        self.visible_sprites.custom_draw()
        self.ui.display()

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

    def run(self):
        if not self.should_display_start_screen:
            self._run_active()
        else:
            self.background_sound.stop()  # make sure it plays again when the game loads
            self.display_start_screen()


class CameraGroup(pygame.sprite.Group):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
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
            for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft + self.offset
                    self.display_surf.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type')
                         and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
