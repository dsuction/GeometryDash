import sys
import pygame as pg
from pygame.display import update

from scenes.scene import Scene
from utils.utils import load_level, get_names_files_directory, paste_image
from assets.game_objects import Button


class LevelMenu(pg.Surface):
    def __init__(self, level, window_size):
        super().__init__(window_size)
        self._window_size = window_size
        self._level = level
        self._buttons_group = pg.sprite.Group()
        self.fill(self._level['color_menu'])
        self._button = Button(self._buttons_group, 'menu/icons/daily_button.png', (300, 300),
                              window_size, (600, 600), 'print')

    def update(self):
        self._buttons_group.draw(self)


class LevelsMenuScene(Scene):
    def __init__(self, window_size) -> None:
        super().__init__(window_size)
        self._levels = {}
        self._button_group = pg.sprite.Group()
        self._buttons = []
        self._levels_menu = []
        self._current_level = 0
        self._is_swap = False
        self._delta_pos = 0
        self._speed_swap = 150
        self._direction = 0
        self._back_to_menu_button = Button(self._button_group, 'levels_menu/icons/back_to_menu_button.png', (100, 100),
                                           window_size, (60, 60), 'return_to_menu')
        self._swipe_left_button = Button(self._button_group, 'levels_menu/icons/swap_left_button.png', (100, 100),
                                         window_size, (80, window_size[1] // 2), 'swap_left')
        self._swipe_right_button = Button(self._button_group, 'levels_menu/icons/swap_right_button.png', (100, 100),
                                          window_size, (window_size[0] - 80, window_size[1] // 2), 'swap_right')
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
        self.swap_level()
        for level in self._levels_menu:
            level.update()
        self._button_group.draw(self._scene)
        self._button_group.update()
        paste_image(self._scene, 'levels_menu/icons/corner_l.png', (400, 400), (200, self._window_size[1] - 200))
        paste_image(self._scene, 'levels_menu/icons/corner_r.png', (400, 400), (self._window_size[0] - 200, self._window_size[1] - 200))
        paste_image(self._scene, 'levels_menu/icons/top_place.png', (1000, 130), (self._window_size[0] // 2, 65))
        self._handle_event()


    def swap_level(self) -> None:
        for i, level in enumerate(self._levels_menu):
            end_x = self._window_size[0] * (i - self._current_level)
            if self._direction == 1:
                x = end_x - self._window_size[0] + self._delta_pos
            elif self._direction == -1:
                x = end_x + self._window_size[0] - self._delta_pos
            else:
                x = end_x
            self._scene.blit(level, (x, 0))
            if self._is_swap:
                self._delta_pos += self._speed_swap
            if 0 > self._delta_pos or self._delta_pos > self._window_size[0]:
                self._is_swap = False
                self._delta_pos = 0
                self._direction = 0

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
        self.check_swap_event()

    def check_swap_event(self) -> None:
        if self._event == 'swap_left':
            self._current_level -= 1
            self._direction = 1
            if self._current_level < 0:
                self._current_level = len(self._levels_menu) - 1
        elif self._event == 'swap_right':
            self._current_level += 1
            self._direction = -1
            if self._current_level >= len(self._levels_menu):
                self._current_level = 0
        else:
            return
        self._is_swap = True
        self._event = ''
