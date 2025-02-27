import sys

from assets.game_objects import Button
from scenes.scene import Scene
from utils.utils import paste_image, load_json, save_json
import pygame as pg


class SkinSelection(Scene):
    def __init__(self, window_size: tuple[int, int]) -> None:
        super().__init__(window_size)
        self._button_group = pg.sprite.Group()
        self._buttons: list[Button] = []
        self._path_settings = 'player/settings/player.json'
        self._back_to_menu_button = Button(self._button_group, 'levels_menu/icons/back_to_menu_button.png',
                                           (100, 100), window_size, (60, 60), 'return_to_menu')
        path_skin = [f'player/icons/cube_skin_{i}.png' for i in range(1, 10 + 1)]
        x, y = round(window_size[0] / 4), round(window_size[1] / 1.9)
        size = 150, 150
        for i in range(10):
            pos = (x + 200 * (i % 5), y + 200 * (i // 5))
            signal = f'select \'{path_skin[i]}\''
            self._buttons.append(Button(self._button_group, path_skin[i], size, self._window_size, pos, signal))
        self.init_ui()

    def init_ui(self) -> None:
        self._buttons.extend([self._back_to_menu_button])

    def update(self) -> None:
        self._handle_event()
        for button in self._buttons:
            button.update()

        pos = (self._window_size[0] // 2, self._window_size[1] // 2)
        paste_image(self._scene, 'menu_skin_selection/icons/backgraund.jpg', self._window_size, pos)

        paste_image(self._scene, 'levels_menu/icons/corner_l.png', (400, 400),
                    (200, self._window_size[1] - 200))
        paste_image(self._scene, 'levels_menu/icons/corner_r.png', (400, 400),
                    (self._window_size[0] - 200, self._window_size[1] - 200))
        self._button_group.draw(self._scene)
        paste_image(self._scene, 'menu_skin_selection/icons/corner_l.png', (400, 400),
                    (200, 200))
        paste_image(self._scene, 'menu_skin_selection/icons/corner_r.png', (400, 400),
                    (self._window_size[0] - 200, 200))

        paste_image(self._scene, 'menu_skin_selection/icons/line.png', (1000, 20),
                    (round(self._window_size[0] / 2), round(self._window_size[1] / 2 - 100)))
        path_active_skin = load_json(self._path_settings)['path_image']
        paste_image(self._scene, path_active_skin, (200, 200),
                    (round(self._window_size[0] / 2), round(self._window_size[1] / 2 - 200)))

        self._button_group.draw(self._scene)

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
                    buttons = self._buttons
                    for button in buttons:
                        if button.is_pressed:
                            self._event = button.signal
        if 'select' in self._event:
            self.select(self._event[self._event.find('\'') + 1:self._event.rfind('\'')])
            self._event = ''

    def select(self, path: str) -> None:
        data = load_json(self._path_settings)
        data['path_image'] = path
        save_json(self._path_settings, data)
