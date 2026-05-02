from enum import Enum, auto

from pygame.constants import (
    K_DOWN,
    K_LEFT,
    K_UP,
    K_RIGHT,
    K_SPACE,
    K_LCTRL,
    K_m,
    K_e,
    K_q,
)


class Controls(Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()
    SELECT = auto()
    ATTACK_ACTION = auto()
    CAST_ACTION = auto()
    SWITCH_WEAPON_ACTION = auto()
    SWITCH_SPELL_ACTION = auto()
    TOGGLE_MENU = auto()


CONTROLS = {
    Controls.RIGHT: K_RIGHT,
    Controls.LEFT: K_LEFT,
    Controls.UP: K_UP,
    Controls.DOWN: K_DOWN,
    Controls.SELECT: K_SPACE,
    Controls.ATTACK_ACTION: K_SPACE,
    Controls.CAST_ACTION: K_LCTRL,
    Controls.SWITCH_WEAPON_ACTION: K_q,
    Controls.SWITCH_SPELL_ACTION: K_e,
    Controls.TOGGLE_MENU: K_m,
}

__all__ = ["CONTROLS", "Controls"]
