import sys
import logging

import pygame

from src.data.images import load_images
from src.data.fonts import init_fonts
from src.systems.scene_manager import SceneManager
from src.scenes.main_world import MainWorld

# from src.debug import debug

logger = logging.getLogger(__name__)


class Level:
    def __init__(self):
        self.load_game()
        self.scene_manager = SceneManager()
        self.scene_manager.register_scene("main_world", MainWorld(self.scene_manager))
        self.scene_manager.go_to_scene("main_world")

        # self.should_display_start_screen = False

    @staticmethod
    def load_game():
        def _load_resource(action, label):
            try:
                action()
            except pygame.error as e:
                logger.error(f"Could not load {label}. Error: {e}")
                pygame.quit()
                sys.exit()
            else:
                logger.info(f"Loaded {label} successfully")

        _load_resource(load_images, "images")
        _load_resource(init_fonts, "fonts")

    def handle_events(self, event):
        self.scene_manager.handle_events(event)

    def run(self, dt):
        # if not self.should_display_start_screen:
        self.scene_manager.update(dt)
        self.scene_manager.draw()
        # else:
        #     audio_manager.stop_sound(
        #         "background"
        #     )  # make sure it plays again when the game loads
