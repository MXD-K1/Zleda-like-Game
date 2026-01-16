from enum import Enum, auto


class Event(Enum):
    CAST_MAGIC = auto()
    CREATE_ATTACK = auto()
    DESTROY_ATTACK = auto()

    GET_PLAYER_DIRECTION = auto()
    GET_PLAYER_RECT = auto()
    GET_PLAYER_WEAPON = auto()

class EventBus:
    def __init__(self):
        self.events = {}

    def subscribe(self, event: Enum, callback):
        if event not in self.events:
            self.events[event] = callback
        else:
            raise ValueError("Event already subscribed.")

    def unsubscribe(self, event: Enum):
        if event in self.events:
            del self.events[event]
        else:
            raise ValueError("Event not subscribed.")

    def emit(self, event: Enum, **kwargs):
        if event not in self.events:
            raise ValueError("Event not subscribed.")
        else:
            return self.events[event](**kwargs)
