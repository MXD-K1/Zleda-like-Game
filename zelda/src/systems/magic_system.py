from enum import Enum
from random import randint

import pygame

from src.settings import TILE_SIZE
from src.systems.audio_system import audio_manager


class MagicAttacks(Enum):  # will be renamed to spells
    HEAL = "heal"
    FLAME = "flame"


class MagicSystem:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def cast(self, player, style, strength, cost, groups):
        if style == MagicAttacks.HEAL.value:
            return self.heal(player, strength, cost, groups[style])
        if style == MagicAttacks.FLAME.value:
            return self.flame(player, cost, groups[style])
        return None

    def heal(self, player, strength, cost, groups):
        if player.energy < cost:
            return None

        audio_manager.play_sound(MagicAttacks.HEAL.value)
        player.health += strength
        player.energy -= cost

        if player.health >= player.stats["health"]:
            player.health = player.stats["health"]

        self.animation_player.create_particles("aura", player.rect.center, groups)
        self.animation_player.create_particles(
            MagicAttacks.HEAL.value,
            player.rect.center + pygame.math.Vector2(0, -60),
            groups,
        )
        return True

    def flame(self, player, cost, groups):
        if player.energy < cost:
            return None

        flame_number = 6
        audio_manager.play_sound(MagicAttacks.FLAME.value)
        player.energy -= cost

        direction_name = player.status.split("_")[0]
        if direction_name == "right":
            direction = pygame.math.Vector2(1, 0)
        elif direction_name == "left":
            direction = pygame.math.Vector2(-1, 0)
        elif direction_name == "up":
            direction = pygame.math.Vector2(0, -1)
        else:
            direction = pygame.math.Vector2(0, 1)

        for i in range(1, flame_number):
            if direction.x:  # horizontal
                offset_x = (direction.x * i) * TILE_SIZE
                x = (
                    player.rect.centerx
                    + offset_x
                    + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                )
                y = player.rect.centery + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                self.animation_player.create_particles(
                    MagicAttacks.FLAME.value, (x, y), groups
                )
            else:  # vertical
                offset_y = (direction.y * i) * TILE_SIZE
                x = player.rect.centerx + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                y = (
                    player.rect.centery
                    + offset_y
                    + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                )
                self.animation_player.create_particles(
                    MagicAttacks.FLAME.value, (x, y), groups
                )

        return True
