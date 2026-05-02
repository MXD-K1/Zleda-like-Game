import logging

import pygame
from src.data.fonts import fonts

logger = logging.getLogger(__name__)


def debug(info, x=10, y=10, color="White"):
    logger.debug(info)
    display_surface = pygame.display.get_surface()
    debug_surf = fonts["debug"].render(str(info), True, color)
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, "Black", debug_rect)
    display_surface.blit(debug_surf, debug_rect)
