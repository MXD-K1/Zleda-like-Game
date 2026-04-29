import pygame

from src.data.sounds import sounds
from src.settings import HITBOX_OFFSET
from src.data.data import weapon_data, magic_data
from src.utils.utils import import_folder, get_assets_dir, wave_value
from src.data.controls import *
from src.entities.entity import Entity
from src.events import EventBus, Event

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, event_bus: EventBus):
        image = pygame.image.load(get_assets_dir() + 'graphics/player/down_idle/idle_down.png').convert_alpha()
        super().__init__(groups, image)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])
        self.obstacle_sprites = obstacle_sprites
        self.event_bus = event_bus

        # graphics
        self.import_assets()
        self.status = 'down'

        # attack
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0  # or None

        self.weapon_index = 0
        self.weapon_names = list(weapon_data.keys())
        self.weapon = self.weapon_names[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        self.magic_index = 0
        self.magic_names = list(magic_data.keys())
        self.magic = self.magic_names[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 0
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        self.weapon_attack_sound = sounds['attack']
        self.weapon_attack_sound.set_volume(0.4)

    # noinspection PyAttributeOutsideInit
    def import_assets(self):
        path = get_assets_dir() + 'graphics/player/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []
        }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(path + animation)

    def _set_vertical_direction(self, keys):
        if keys[CONTROLS[Controls.UP]]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[CONTROLS[Controls.DOWN]]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

    def _set_horizontal_direction(self, keys):
        if keys[CONTROLS[Controls.RIGHT]]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[CONTROLS[Controls.LEFT]]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

    def _start_attack(self):
        self.attacking = True
        self.attack_time = pygame.time.get_ticks()
        self.event_bus.publish(Event.CREATE_ATTACK)
        self.weapon_attack_sound.play()

    def _cast_magic(self):
        self.attacking = True
        self.attack_time = pygame.time.get_ticks()

        magic = magic_data[self.magic]
        strength = magic['strength'] + self.stats['magic']
        cost = magic['cost']

        self.event_bus.publish(Event.CAST_MAGIC, style=self.magic, strength=strength, cost=cost)

    def _select_next_weapon(self):
        if self.weapon_index < len(self.weapon_names) - 1:
            self.weapon_index += 1
        else:
            self.weapon_index = 0
        self.weapon = self.weapon_names[self.weapon_index]

    def _select_next_magic(self):
        if self.magic_index < len(self.magic_names) - 1:
            self.magic_index += 1
        else:
            self.magic_index = 0
        self.magic = self.magic_names[self.magic_index]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            # movement
            self._set_vertical_direction(keys)
            self._set_horizontal_direction(keys)

            # attack
            if keys[CONTROLS[Controls.ATTACK_ACTION]] and not self.attacking:
                self._start_attack()

            # magic
            if keys[CONTROLS[Controls.CAST_ACTION]] and not self.attacking:
                self._cast_magic()

            if keys[CONTROLS[Controls.SWITCH_WEAPON_ACTION]] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self._select_next_weapon()

            if keys[CONTROLS[Controls.SWITCH_SPELL_ACTION]] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                self._select_next_magic()

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status and 'attack' not in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x, self.direction.y = 0, 0
            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.event_bus.publish(Event.DESTROY_ATTACK)

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.002 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def add_exp(self, amount):
        self.exp += amount

    # ---------- Getters -------------

    def get_direction(self):
        return self.status.split('_')[0]

    def get_rect(self):
        return self.rect

    def get_weapon(self):
        return self.weapon

    def get_exp(self):
        return self.exp

    def get_health(self):
        return self.health

    def get_energy(self):
        return self.energy

    def get_stats(self):
        return {
            'stats': self.stats,
            'max_stats': self.max_stats,
            'upgrade_cost': self.upgrade_cost
        }

    def get_attack_info(self):
        return {
            'weapon_index': self.weapon_index,
            'magic_index': self.magic_index,
            'can_switch_weapon': self.can_switch_weapon,
            'can_switch_magic': self.can_switch_magic
        }

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    # --------------------------------

    def update(self):
        self.input()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
