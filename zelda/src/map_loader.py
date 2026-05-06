from pytmx import load_pygame

from src.sprites.tile import Tile
from src.settings import TILE_SIZE
from src.sprites.object import Object
from src.entities.player import Player
from src.entities.enemy import Enemy


class MapLoader:
    def __init__(self, level):
        self.level = level
        self.groups = [
            level.visible_sprites,
            level.obstacle_sprites,
            level.attack_sprites,
            level.attackable_sprites,
        ]

        self.cur_map = None

    def get_map_info(self):
        return {
            "width": TILE_SIZE * self.cur_map.width,
            "height": TILE_SIZE * self.cur_map.height
        }

    def empty_groups(self):
        for group in self.groups:
            group.empty()

    # noinspection PyTypeChecker,PyUnresolvedReferences
    def load_map(self, map_path):
        self.empty_groups()
        self.cur_map = load_pygame(map_path)
        player = None

        for x, y, surf in self.cur_map.get_layer_by_name("Floor").tiles():
            Tile(
                (x * TILE_SIZE, y * TILE_SIZE),
                [self.level.visible_sprites],
                "grass",
                surf,
            )

        for x, y, surf in self.cur_map.get_layer_by_name("Grass").tiles():
            Tile(
                (x * TILE_SIZE, y * TILE_SIZE),
                [
                    self.level.visible_sprites,
                    self.level.obstacle_sprites,
                    self.level.attackable_sprites,
                ],
                "grass",
                surf,
            )

        for x, y, surf in self.cur_map.get_layer_by_name("Objects").tiles():
            Object(
                (x * TILE_SIZE, y * TILE_SIZE),
                [self.level.visible_sprites, self.level.obstacle_sprites],
                "object",
                surf,
            )

        for x, y, surf in self.cur_map.get_layer_by_name("FloorBlocks").tiles():
            Tile(
                (x * TILE_SIZE, y * TILE_SIZE),
                [self.level.obstacle_sprites],
                "invisible",
            )

        for obj in self.cur_map.get_layer_by_name("Entity-Pos"):
            if obj.name == "player":
                player = Player(
                    (obj.x, obj.y),
                    [self.level.visible_sprites],
                    self.level.obstacle_sprites,
                    self.level.event_bus,
                )
            else:
                Enemy(
                    obj.name,
                    (obj.x, obj.y),
                    [self.level.visible_sprites, self.level.attackable_sprites],
                    self.level.obstacle_sprites,
                    self.level.combat.damage_player,
                    self.level.trigger_death_particles,
                    self.level.combat.add_exp,
                )

        return player
