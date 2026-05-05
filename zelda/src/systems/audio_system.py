import logging

from pygame import mixer

from src.utils.utils import get_assets_dir

__all__ = ["audio_manager"]

logger = logging.getLogger(__name__)


class AudioManager:
    instance = None
    initiated = False

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if self.initiated:
            return

        self.__sounds = {}
        self.initiated = True

    def load_sounds(self):
        try:
            self.__sounds.update(
                {
                    "background": mixer.Sound(get_assets_dir() + "audio/main.ogg"),
                    "heal": mixer.Sound(get_assets_dir() + "audio/heal.wav"),
                    "flame": mixer.Sound(get_assets_dir() + "audio/flame.wav"),
                    "player.attack": mixer.Sound(get_assets_dir() + "audio/sword.wav"),
                    "monster.death": mixer.Sound(get_assets_dir() + "audio/death.wav"),
                    "monster.hit": mixer.Sound(get_assets_dir() + "audio/hit.wav"),
                }
            )

            self.adjust_sounds()
        except Exception:
            logger.exception("Sounds could not be loaded")
            raise
        else:
            logger.info("Loaded sounds successfully")

    def adjust_sounds(self):
        self.__sounds["background"].set_volume(0.5)
        self.__sounds["monster.death"].set_volume(0.6)
        self.__sounds["monster.hit"].set_volume(0.6)
        self.__sounds["player.attack"].set_volume(0.4)

    def play_sound(self, name: str, endlessly: bool = False):
        try:
            times = 0 if not endlessly else -1
            self.__sounds[name].play(times)
        except KeyError:
            logger.warning(f"Sound {name} not found")

    def stop_sound(self, name: str):
        try:
            self.__sounds[name].stop()
        except KeyError:
            logger.warning(f"Sound {name} not found")


audio_manager = AudioManager()
