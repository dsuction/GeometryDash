import sys
import pygame as pg
from tools.tools import load_music, paste_image
from scenes.scene import Scene
from assets.game_objects import Button, Background, Platforms, GameObject


class MenuScene(Scene):
    color_background = 0

    def __init__(self, window_size: tuple[int, int]) -> None:
        super().__init__(window_size)
        self._objects: list[GameObject] = []
        self._buttons: list[Button] =  []
        self._all_sprite = pg.sprite.Group()
        self._background = Background(window_size, 'menu/icons/background.png')
        self._platforms = Platforms(window_size)
        self._start_button = Button(self._all_sprite, 'menu/icons/start_button.png',
                                    (window_size[1] // 3, window_size[1] // 3), window_size,
                                    (window_size[0] // 2, window_size[1] // 2 - 20), 'open_levels_menu')
        self._exit_button = Button(self._all_sprite, 'menu/icons/exit_button.png',
                                   (window_size[1] // 15, window_size[1] // 15), window_size,
                                   (40, 40), 'open_exit_menu')
        load_music('menu\sounds\menuLoop.mp3')
        pg.mixer.music.play(-1)
        self._event = ''
        self.init_ui()

    def init_ui(self) -> None:
        self._objects.append(self._background)
        self._objects.append(self._platforms)
        self._objects.append(self._start_button)
        self._objects.append(self._exit_button)
        self._buttons.append(self._start_button)
        self._buttons.append(self._exit_button)

    def update(self) -> None:
        self._handle_event()
        for ob in self._objects:
            ob.update()
        MenuScene.color_background = (MenuScene.color_background + 1) if MenuScene.color_background <= 1529 else 0
        self._scene.fill(self.set_color(MenuScene.color_background))
        self._scene.blit(self._background, (0, 0))
        self._scene.blit(self._platforms, (0, self._window_size[1] - self._window_size[1] // 3))
        paste_image(self._scene, 'menu/icons/gd.jpg', (704, 545), (self._window_size[0] // 2, self._window_size[1] // 5), color_key=-1)
        self._all_sprite.draw(self._scene)

    def _handle_event(self) -> None:
        self._event = ''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                lkm = 1
                if event.button == lkm:
                    for button in self._buttons:
                        if button.is_pressed:
                            self._event = button.signal

    @staticmethod
    def set_color(color: int) -> pg.color:
        rgb = [0, 0, 0]
        if color <= 255:
            rgb[0] = 255
            rgb[1] = color
            rgb[2] = 0
        elif 255 < color <= 510:
            rgb[0] = 510 - color
            rgb[1] = 255
            rgb[2] = 0
        elif 510 < color <= 765:
            rgb[0] = 0
            rgb[1] = 255
            rgb[2] = color - 510
        elif 765 < color <= 1020:
            rgb[0] = 0
            rgb[1] = 1020 - color
            rgb[2] = 255
        elif 1020 < color <= 1275:
            rgb[0] = color - 1020
            rgb[1] = 0
            rgb[2] = 255
        elif 1275 < color <= 1530:
            rgb[0] = 255
            rgb[1] = 0
            rgb[2] = 1530 - color
        return pg.color.Color(*rgb)
