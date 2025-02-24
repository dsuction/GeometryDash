import pygame as pg
from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, window_size: tuple[int, int]) -> None:
        self._scene = pg.Surface(window_size)
        self._event = ''
        self._window_size = window_size

    @abstractmethod
    def init_ui(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def _handle_event(self):
        pass

    @property
    def scene(self) -> pg.Surface:
        return self._scene

    @property
    def event(self) -> str:
        return self._event
