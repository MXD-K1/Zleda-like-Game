from pytmx import load_pygame

from tile import Tile
from settings import TILE_SIZE
from object import Object
from player import Player
from enemy import Enemy


class MapLoader:
    def __init__(self, level):
        self.level = level
        self.groups = [level.visible_sprites, level.obstacle_sprites, level.attack_sprites, level.attackable_sprites]

    def empty_groups(self):
        for group in self.groups:
            group.empty()

    # noinspection PyTypeChecker,PyUnresolvedReferences
    def load_map(self, map_path):
        self.empty_groups()
        map_ = load_pygame(map_path)

        for x, y, surf in map_.get_layer_by_name('Floor').tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE),
                 [self.level.visible_sprites], 'grass', surf)

        for x, y, surf in map_.get_layer_by_name('Grass').tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE),
                 [self.level.visible_sprites, self.level.obstacle_sprites, self.level.attackable_sprites],
                 'grass', surf)

        for x, y, surf in map_.get_layer_by_name('Objects').tiles():
            Object((x * TILE_SIZE, y * TILE_SIZE), [self.level.visible_sprites, self.level.obstacle_sprites],
                   'object', surf)

        for x, y, surf in map_.get_layer_by_name('FloorBlocks').tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE), [self.level.obstacle_sprites], 'invisible')

        for obj in map_.get_layer_by_name('Entity-Pos'):
            if obj.name == "player":
                self.player = Player((obj.x, obj.y), [self.level.visible_sprites],
                                     self.level.obstacle_sprites, self.level.event_bus)
            else:
                Enemy(obj.name, (obj.x, obj.y), [self.level.visible_sprites, self.level.attackable_sprites],
                      self.level.obstacle_sprites, self.level.damage_player, self.level.trigger_death_particles,
                      self.level.add_exp)
