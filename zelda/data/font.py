from typing import Literal

from pygame.font import Font

from zelda.utils.utils import get_assets_dir

fonts = {}

def init_fonts():
    local_fonts = {
        'joystix': {
            'small': Font(get_assets_dir() + 'fonts/joystix.ttf'),
            'medium': Font(get_assets_dir() + 'fonts/joystix.ttf', 18),
            'large': Font(get_assets_dir() + 'fonts/joystix.ttf')
        },
    }

    fonts.update(local_fonts)

def get_font(name: str, size:  Literal['small', 'medium', 'large']):
    return fonts[name][size]
