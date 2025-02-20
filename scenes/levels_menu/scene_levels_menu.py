import sys
import pygame as pg
from scenes.scene import Scene


class LevelsMenuScene(Scene):
    def __init__(self, size):
        super().__init__(size)

    def init_ui(self):
        pass

    def update(self):
        self._handle_event()

    def _handle_event(self):
        self._event = ''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self._event = 'return_to_menu'
