import pygame

from zelda.events import Event, EventBus
from zelda.settings import *
from zelda.data.data import weapon_data, magic_data
from zelda.data.color import *


class UI:
    def __init__(self, event_bus: EventBus):
        self.display_surf = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.event_bus = event_bus

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon_graphic = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon_graphic)

        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic_graphic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic_graphic)

    def show_bar(self, current_amount, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surf, UI_BG_COLOR, bg_rect)

        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.display_surf, color, current_rect)
        pygame.draw.rect(self.display_surf, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=(self.display_surf.get_size()[0] - 20,
                                                    self.display_surf.get_size()[1] - 20))
        pygame.draw.rect(self.display_surf, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surf.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surf, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched)  # weapon
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surf.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(93, 632, has_switched)  # magic
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surf.blit(magic_surf, magic_rect)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surf, UI_BG_COLOR, bg_rect)
        if not has_switched:
            pygame.draw.rect(self.display_surf, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surf, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def display(self, player):
        # TODO: get rid of the player arg
        player_stats = self.event_bus.emit(Event.GET_PLAYER_STATS)
        self.show_bar(self.event_bus.emit(Event.GET_PLAYER_HEALTH), player_stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(self.event_bus.emit(Event.GET_PLAYER_ENERGY), player_stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_exp(self.event_bus.emit(Event.GET_PLAYER_EXP))
        self.weapon_overlay(player.weapon_index, player.can_switch_weapon)
        self.magic_overlay(player.magic_index, player.can_switch_magic)
