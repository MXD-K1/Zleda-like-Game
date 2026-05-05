import logging

import pygame

from src.data.fonts import get_font
from src.data.color import (
    TEXT_COLOR,
    TEXT_COLOR_SELECTED,
    BAR_COLOR,
    BAR_COLOR_SELECTED,
    UI_BG_COLOR,
    UPGRADE_BG_COLOR_SELECTED,
    UI_BORDER_COLOR,
)
from src.data.controls import Controls, CONTROLS
from src.events import Event, EventBus

logger = logging.getLogger(__name__)


class Upgrade:
    def __init__(self, event_bus: EventBus):
        self.display_surf = pygame.display.get_surface()
        if self.display_surf is None:
            logger.error("Display surface is not initialized.")
            raise Exception("Display surface is not initialized.")

        self.event_bus = event_bus
        player_stats = self.event_bus.publish(Event.GET_PLAYER_STATS)

        self.attribute_names = list(player_stats["stats"].keys())
        self.attribute_number = len(self.attribute_names)
        self.max_values = list(player_stats["max_stats"].values())
        self.font = get_font("joystix", "medium")

        # item dimensions
        self.height = self.display_surf.get_height() * 0.8
        self.width = self.display_surf.get_width() // (self.attribute_number + 1)
        self.create_items()

        # selection_system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if (
                keys[CONTROLS[Controls.RIGHT]]
                and self.selection_index < self.attribute_number - 1
            ):
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[CONTROLS[Controls.LEFT]] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[CONTROLS[Controls.SELECT]]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self._apply_upgrade(self.selection_index)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    # noinspection PyAttributeOutsideInit
    def create_items(self):
        self.item_list = []

        for item_number, index in enumerate(range(self.attribute_number)):
            top = self.display_surf.get_height() * 0.1

            full_width = self.display_surf.get_width()
            increment = full_width // self.attribute_number
            left = (item_number * increment) + (increment - self.width) // 2

            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()
        player_stats = self.event_bus.publish(Event.GET_PLAYER_STATS)
        stats = player_stats["stats"]
        max_stats = player_stats["max_stats"]
        upgrade_cost = player_stats["upgrade_cost"]
        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = stats[name]
            max_value = max_stats[name]
            cost = upgrade_cost[name]
            item.display(
                self.display_surf, self.selection_index, name, value, max_value, cost
            )

    def _apply_upgrade(self, index):
        player_stats = self.event_bus.publish(Event.GET_PLAYER_STATS)
        stats = player_stats["stats"]
        max_stats = player_stats["max_stats"]
        upgrade_cost = player_stats["upgrade_cost"]

        upgrade_attribute = self.attribute_names[index]
        cost = upgrade_cost[upgrade_attribute]
        exp = self.event_bus.publish(Event.GET_PLAYER_EXP)

        if exp >= int(cost) and stats[upgrade_attribute] < max_stats[upgrade_attribute]:
            self.event_bus.publish(Event.ADD_EXP, amount=-cost)
            stats[upgrade_attribute] *= 1.2
            upgrade_cost[upgrade_attribute] *= 1.4

        if stats[upgrade_attribute] > max_stats[upgrade_attribute]:
            stats[upgrade_attribute] = max_stats[upgrade_attribute]


class Item:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        # title text
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(
            midtop=self.rect.midtop + pygame.math.Vector2(0, 20)
        )

        # cost text
        cost_surf = self.font.render(str(int(cost)), False, color)
        cost_rect = cost_surf.get_rect(
            midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20)
        )

        # draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(
            top[0] - 15, bottom[1] - relative_number, 30, 10
        )  # top[0] == bottom[0]

        # draw_elements
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        self.display_names(surface, name, cost, self.index == selection_num)
        self.display_bar(surface, value, max_value, self.index == selection_num)
