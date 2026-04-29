import sys
import logging

import pygame

from src.ui import UI
from src.particles import AnimationPlayer
from src.magic import MagicPlayer
from src.upgrade import Upgrade
from src.map_loader import MapLoader
from src.utils.utils import get_assets_dir
from src.events import EventBus, Event
from src.data.images import load_images
from src.data.sounds import load_sounds, sounds
from src.data.fonts import init_fonts
from src.systems.combat_system import Combat
from src.systems.camera_system import Camera

# from src.debug import debug

logger = logging.getLogger(__name__)

class Level:
    def __init__(self):
        self.load_game()

        self.display_surf = pygame.display.get_surface()
        self.event_bus = EventBus()
        self.game_paused = False

        # sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.cam = Camera(self.visible_sprites, self.event_bus)

        # attack
        self.current_attack = None

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        # sound
        self.background_sound = sounds['background']
        self.background_sound.set_volume(0.5)
        self.background_sound.play(-1)

        self.combat = Combat(self.event_bus, self.animation_player, self.magic_player, self.attack_sprites, self.attackable_sprites, self.visible_sprites)
        self.map_loader = MapLoader(self)
        self.player = self._load_map('map.tmx')
        self.combat.set_player(self.player)

        # events
        self.subscribe_events()

        self.ui = UI(self.event_bus)
        self.upgrade = Upgrade(self.event_bus)
        self.should_display_start_screen = False

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
        except pygame.error as e:
            logger.error(f'Could not load map. Error: {e}')
            pygame.quit()
            sys.exit()

    def subscribe_events(self):
        self.event_bus.subscribe(Event.GET_PLAYER_DIRECTION, self.player.get_direction)
        self.event_bus.subscribe(Event.GET_PLAYER_RECT, self.player.get_rect)
        self.event_bus.subscribe(Event.GET_PLAYER_WEAPON, self.player.get_weapon)
        self.event_bus.subscribe(Event.GET_PLAYER_EXP, self.player.get_exp)
        self.event_bus.subscribe(Event.GET_PLAYER_HEALTH, self.player.get_health)
        self.event_bus.subscribe(Event.GET_PLAYER_ENERGY, self.player.get_energy)
        self.event_bus.subscribe(Event.GET_PLAYER_STATS, self.player.get_stats)
        self.event_bus.subscribe(Event.GET_PLAYER_ATTACK_INFO, self.player.get_attack_info)

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def _run_active(self):
        self.cam.custom_draw()
        self.ui.display()

        if self.game_paused:
            self.upgrade.display()
        else:
            self.cam.update()
            self.cam.enemy_update(self.player)
            self.combat.player_attack_logic()

    def run(self):
        if not self.should_display_start_screen:
            self._run_active()
        else:
            self.background_sound.stop()  # make sure it plays again when the game loads
            self.display_start_screen()
