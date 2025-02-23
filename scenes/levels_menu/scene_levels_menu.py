import sys
import pygame as pg
from scenes.scene import Scene
from tools.tools import load_level, get_names_files_directory
import json


class LevelsMenuScene(Scene):
    def __init__(self, size):
        super().__init__(size)
        self.init_ui()

    def init_ui(self):
        self._scene.fill('blue')
    
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
