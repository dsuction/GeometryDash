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
        self._button = None

    def update(self):
        pass


class LevelsMenuScene(Scene):
    def __init__(self, window_size) -> None:
        super().__init__(window_size)
        self._levels = {}
        self._button_group = pg.sprite.Group()
        self._buttons = []
        self._levels_menu = []
        self._current_level = 0
        self._back_to_menu_button = Button(self._button_group, 'menu/icons/x_button.png', (100, 100),
                                           window_size, (0, 0), 'return_to_menu')
        self._swipe_left_button = Button(self._button_group, 'menu/icons/x_button.png', (100, 100),
                                         window_size, (100, 100), 'swap_left')
        self._swipe_right_button = Button(self._button_group, 'menu/icons/x_button.png', (100, 100),
                                          window_size, (500, 500), 'swap_right')
        self.init_ui()

    def init_ui(self) -> None:
        for button in [self._back_to_menu_button, self._swipe_left_button, self._swipe_right_button]:
            self._buttons.append(button)
        for file in get_names_files_directory('levels'):
            color = load_level('levels/' + file)['color_menu']
            self._levels[file] = {'name': file, 'color_menu': color}
        for level in self._levels.values():
            self._levels_menu.append(LevelMenu(level, self._window_size))

    def update(self) -> None:
        print(len(self._levels_menu))
        self._scene.fill('black')
        for i, level in enumerate(self._levels_menu):
            print(self._window_size[0] * (i - self._current_level))
            self._scene.blit(level, (self._window_size[0] * (i - self._current_level), 0))
        self._button_group.draw(self._scene)
        self._button_group.update()
        self._handle_event()

    def _handle_event(self) -> None:
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
        if self._event == 'swap_left':
            self._current_level -= 1
            if self._current_level < 0:
                self._current_level = len(self._levels_menu) - 1
            self._event = ''
        elif self._event == 'swap_right':
            self._current_level += 1
            if self._current_level >= len(self._levels_menu):
                self._current_level = 0
            self._event = ''

    def swap_level(self):
        pass
