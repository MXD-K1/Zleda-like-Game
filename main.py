import logging
import sys

import pygame

from zelda.log import setup_logging
from zelda.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE
from zelda.data.color import WATER_COLOR
from zelda.data.controls import *
from zelda.level import Level

# from debug import debug

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
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

def run_game():
    try:
        setup_logging()
        game = Game()
        game.run()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        logging.error(e)
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    run_game()
