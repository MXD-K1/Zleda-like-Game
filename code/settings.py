from code.utils.utils import get_assets_dir

# game setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 64

HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0
}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = get_assets_dir() + 'fonts/joystix.ttf'
UI_FONT_SIZE = 18

LAYERS = {
    'water': 0,
    'floor': 1,
    'main': 2,
}

del get_assets_dir
