import pygame
from zelda.data.fonts import fonts

def debug(info, x=10, y=10, color='White'):
    display_surface = pygame.display.get_surface()
    debug_surf = fonts[''].render(str(info), True, color)
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, 'Black', debug_rect)
    display_surface.blit(debug_surf, debug_rect)
