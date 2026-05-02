import logging
import sys

import pygame

from src.log import setup_logging
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE
from src.data.color import WATER_COLOR
from src.data.controls import CONTROLS, Controls
from src.level import Level

# from src.debug import debug

logging.getLogger(__name__)


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == CONTROLS[Controls.TOGGLE_MENU]:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.clock.tick(FPS)
            self.level.run()
            pygame.display.update()


def run_game():
    try:
        setup_logging()
        game = Game()
        game.run()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        logging.exception("Unexpected Exception")
        raise e


if __name__ == "__main__":
    run_game()
