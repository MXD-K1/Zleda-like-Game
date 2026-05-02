import logging
from random import randint

import pygame

from src.events import Event
from src.weapon import Weapon

logger = logging.getLogger(__name__)


class Combat:
    def __init__(
        self,
        event_bus,
        animation_player,
        magic_player,
        attack_sprites,
        attackable_sprites,
        visible_sprites,
    ):
        self.current_attack = None

        self.player = None
        self.event_bus = event_bus
        self.animation_player = animation_player
        self.magic_player = magic_player
        self.attack_sprites = attack_sprites
        self.attackable_sprites = attackable_sprites
        self.visible_sprites = visible_sprites

    def set_player(self, player):
        self.player = player
        self.subscribe_events()

    def subscribe_events(self):
        self.event_bus.subscribe(Event.CREATE_ATTACK, self.create_attack)
        self.event_bus.subscribe(Event.DESTROY_ATTACK, self.destroy_attack)
        self.event_bus.subscribe(Event.CAST_MAGIC, self.create_magic)
        self.event_bus.subscribe(Event.ADD_EXP, self.player.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(
            [self.visible_sprites, self.attack_sprites], self.event_bus
        )

    def create_magic(self, style, strength, cost):
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        elif style == "flame":
            self.magic_player.flame(
                self.player, cost, [self.visible_sprites, self.attack_sprites]
            )

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def add_exp(self, amount):
        self.event_bus.publish(Event.ADD_EXP, amount=amount)
        self.player.exp += amount

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

            # particles
            self.animation_player.create_particles(
                attack_type, self.player.rect.center, [self.visible_sprites]
            )

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False
                )
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 70)
                            for _ in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(
                                    pos - offset, [self.visible_sprites]
                                )
                            target_sprite.kill()
                        else:  # enemy
                            target_sprite.get_damage(
                                self.player, attack_sprite.sprite_type
                            )
