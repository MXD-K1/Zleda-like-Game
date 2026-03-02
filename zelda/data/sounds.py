from pygame import mixer

from zelda.utils.utils import get_assets_dir

sounds = {}

def load_sounds():
    loaded_sounds = {
        'background': mixer.Sound(get_assets_dir() + 'audio/main.ogg'),
        'heal': mixer.Sound(get_assets_dir() + 'audio/heal.wav'),
        'flame': mixer.Sound(get_assets_dir() + 'audio/flame.wav'),
        'attack': mixer.Sound(get_assets_dir() + 'audio/sword.wav'),
    }

    sounds.update(loaded_sounds)
