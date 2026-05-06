from abc import ABC, abstractmethod

import pygame


class Scene(ABC):
    def __init__(self, manager):
        self.display_sur = pygame.display.get_surface()
        self.manager: SceneManager = manager

    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self):
        pass


class SceneManager:
    def __init__(self):
        self.scenes: dict[str, Scene] = {}

        self.cur_scene: Scene | None = None
        self.prev_scene: Scene | None = None

    def register_scene(self, scene_name: str, scene: Scene):
        self.scenes[scene_name] = scene

    def go_to_scene(self, scene: str):
        self.prev_scene = self.cur_scene
        self.cur_scene = self.scenes[scene]

    def go_backward(self):
        self.cur_scene = self.prev_scene
        self.prev_scene = None

    def handle_events(self):
        self.cur_scene.handle_events()

    def update(self, dt: float):
        self.cur_scene.update(dt)

    def draw(self):
        self.cur_scene.draw()
