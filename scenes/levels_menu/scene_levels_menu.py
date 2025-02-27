import sys
import pygame as pg

from scenes.scene import Scene
from utils.utils import load_json, get_names_files_directory, paste_image
from assets.game_objects import Button


class LevelMenu(pg.Surface):
    def __init__(self, level: dict, window_size: tuple[int, int], path_image: str):
        super().__init__(window_size)
        self._window_size = window_size
        self._level = level
        self._name_level = self._level['name']
        self._buttons_group = pg.sprite.Group()
        self.fill(self._level['color_menu'])
        self.button = Button(self._buttons_group, path_image, (900, 300),
                              window_size, (window_size[0] // 2, window_size[1] // 2), 'open_level')
        self._event = ''

    def update(self):
        if self.button.is_pressed:
            self._event: str = self.button.signal + self._level['name']
        self.fill(self._level['color_menu'])
        self._buttons_group.update()
        self._buttons_group.draw(self)

    @property
    def event(self):
        return self._event



class LevelsMenuScene(Scene):
    def __init__(self, window_size: tuple[int, int]) -> None:
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

        self._back_to_menu_button = Button(self._button_group, 'levels_menu/icons/back_to_menu_button.png',
                                           (100, 100), window_size, (60, 60), 'return_to_menu')

        self._swipe_left_button = Button(self._button_group, 'levels_menu/icons/swap_left_button.png',
                                         (100, 200), window_size, (80, window_size[1] // 2),
                                         'swap_left')

        self._swipe_right_button = Button(self._button_group, 'levels_menu/icons/swap_right_button.png',
                                          (100, 200), window_size, (window_size[0] - 80, window_size[1] // 2),
                                          'swap_right')
        self._paths = {}
        self.init_ui()

    def init_ui(self) -> None:
        for button in [self._back_to_menu_button, self._swipe_left_button, self._swipe_right_button]:
            self._buttons.append(button)
        for file in get_names_files_directory('levels'):
            data = load_json('levels/' + file)
            color = data['color_menu']
            path_image = data['path_image']
            self._paths[file] = path_image
            self._levels[file] = {'name': file, 'color_menu': color}
        for file in self._levels.keys():
            level = self._levels[file]
            path_image = self._paths[file]
            self._levels_menu.append(LevelMenu(level, self._window_size, path_image))

    def update(self) -> None:
        self._handle_event()
        self._scene.fill('black')
        self.swap_level()
        for level in self._levels_menu:
            level.update()
        self._button_group.draw(self._scene)
        self._button_group.update()

        paste_image(self._scene, 'levels_menu/icons/corner_l.png', (400, 400),
                    (200, self._window_size[1] - 200))

        paste_image(self._scene, 'levels_menu/icons/corner_r.png', (400, 400),
                    (self._window_size[0] - 200, self._window_size[1] - 200))

        paste_image(self._scene, 'levels_menu/icons/top_place.png', (1000, 130),
                    (self._window_size[0] // 2, 65))

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
                for level in self._levels_menu:
                    if level.event:
                        self._event = level.event
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
