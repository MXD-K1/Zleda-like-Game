# game setup
GAME_TITLE = 'Zelda'
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
SCALE_FACTOR = 4  # From 16 to 64
TILE_SIZE = 16 * SCALE_FACTOR

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

LAYERS = {
    'water': 0,
    'floor': 1,
    'main': 2,
}
