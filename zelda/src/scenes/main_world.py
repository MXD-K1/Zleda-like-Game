import logging
import sys

import pygame

from src.data.controls import CONTROLS, Controls
from src.events import EventBus, Event
from src.map_loader import MapLoader
from src.particles import AnimationPlayer
from src.systems.scene_manager import Scene
from src.systems.audio_system import audio_manager
from src.systems.camera_system import Camera
from src.systems.combat_system import Combat
from src.systems.magic_system import MagicSystem
from src.ui import UI
from src.upgrade import Upgrade
from src.utils.utils import get_assets_dir

logger = logging.getLogger(__name__)


class MainWorld(Scene):
    def __init__(self, manager):
        super().__init__(manager)

        self.display_surf = pygame.display.get_surface()
        self.event_bus = EventBus()
        self.game_paused = False

        # sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # attack
        self.current_attack = None

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_system = MagicSystem(self.animation_player)

        audio_manager.play_sound("background", True)

        self.combat = Combat(
            self.event_bus,
            self.animation_player,
            self.magic_system,
            self.attack_sprites,
            self.attackable_sprites,
            self.visible_sprites,
        )
        self.map_loader = MapLoader(self)
        self.player = self._load_map("map.tmx")
        self.combat.set_player(self.player)

        map_info = self.map_loader.get_map_info()

        self.cam = Camera(
            map_info | {
                "drawable_sprites": self.visible_sprites
            }, self.event_bus)

        # events
        self.subscribe_events()

        self.ui = UI(self.event_bus)
        self.upgrade = Upgrade(self.event_bus)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == CONTROLS[Controls.TOGGLE_MENU]:
                self.toggle_menu()

    def update(self, dt):
        if not self.game_paused:
            self.cam.update()
            self.cam.enemy_update(self.player)
            self.combat.player_attack_logic()

    def draw(self):
        self.cam.custom_draw(self.player)
        self.ui.display()

        if self.game_paused:
            self.upgrade.display()

    def subscribe_events(self):
        self.event_bus.subscribe(Event.GET_PLAYER_DIRECTION, self.player.get_direction)
        self.event_bus.subscribe(Event.GET_PLAYER_RECT, self.player.get_rect)
        self.event_bus.subscribe(Event.GET_PLAYER_WEAPON, self.player.get_weapon)
        self.event_bus.subscribe(Event.GET_PLAYER_EXP, self.player.get_exp)
        self.event_bus.subscribe(Event.GET_PLAYER_HEALTH, self.player.get_health)
        self.event_bus.subscribe(Event.GET_PLAYER_ENERGY, self.player.get_energy)
        self.event_bus.subscribe(Event.GET_PLAYER_STATS, self.player.get_stats)
        self.event_bus.subscribe(
            Event.GET_PLAYER_ATTACK_INFO, self.player.get_attack_info
        )

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(
            particle_type, pos, [self.visible_sprites]
        )

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def _load_map(self, map_name):
        try:
            player = self.map_loader.load_map(get_assets_dir() + f"maps/{map_name}")
            return player
        except pygame.error as e:
            logger.error(f"Could not load map. Error: {e}")
            pygame.quit()
            sys.exit()
