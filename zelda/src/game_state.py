class GameState:
    instance = None  # singleton

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)

    def __init__(self):
        if self.instance:
            return  # Do not re-init

        self.current_scene = None

        # TODO
