import sys

import pygame

from zelda.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from zelda.data.color import WATER_COLOR
from zelda.level import Level
from zelda.data.font import init_fonts

# from debug import debug

class Game:
    def __init__(self):
        # general setup
        pygame.init()
        init_fonts()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        sys.exit()
