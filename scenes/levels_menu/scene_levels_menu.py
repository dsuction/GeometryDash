import sys
import pygame as pg

from scenes.scene import Scene
from utils.utils import load_level, get_names_files_directory
from assets.game_objects import Button


class LevelMenu(pg.Surface):
    def __init__(self, level, window_size):
        super().__init__(window_size)
        self._window_size = window_size
        self._level = level
        self.fill(self._level['color_menu'])

    def update(self):
        pass


class LevelsMenuScene(Scene):
    def __init__(self, window_size):
        super().__init__(window_size)
        self._levels = {}
        self._button_group = pg.sprite.Group()
        self._buttons = []
        self._back_to_menu_button = Button(self._button_group, 'menu/icons/x_button.png', (100, 100),
                                           window_size, (0, 0), 'return_to_menu')
        self._swipe_left_button = Button(self._button_group, 'menu/icons/x_button.png', (100, 100),
                                         window_size, (100, 100), 'swap_left')
        self._swipe_right_button = Button(self._button_group, 'menu/icons/x_button.png', (100, 100),
                                          window_size, (500, 500), 'swap_right')
        self.init_ui()

    def init_ui(self):
        self._buttons.append(self._back_to_menu_button)
        for file in get_names_files_directory('levels'):
            color = load_level('levels/' + file)['color_menu']
            self._levels['file'] = {'name': file, 'color_menu': color}

    def swap_level(self):
        pass

    def update(self):
        self._button_group.draw(self._scene)
        self._button_group.update()
        self._handle_event()

    def _handle_event(self):
        self._event = ''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self._event = 'return_to_menu'
            elif event.type == pg.MOUSEBUTTONDOWN:
                lkm = 1
                if event.button == lkm:
                    for button in self._buttons:
                        if button.is_pressed:
                            self._event = button.signal
