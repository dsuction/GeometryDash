import sys
import pygame as pg
from utils.utils import load_music, paste_image
from scenes.scene import Scene
from assets.game_objects import Button, Background, Platforms, GameObject, ComingSoon


class MenuScene(Scene):
    color_background = 0

    def __init__(self, window_size: tuple[int, int]) -> None:
        super().__init__(window_size)
        self._objects: list[GameObject] = []
        self._buttons: list[Button] = []
        self._all_sprite = pg.sprite.Group()
        self._exit_sprites = pg.sprite.Group()
        self._exit_menu_buttons: list[Button] = []
        self._background = Background(window_size, 'menu/icons/background.png')
        self._platforms = Platforms(window_size)
        self._is_show_exit_menu = False

        self._start_button = Button(self._all_sprite, 'menu/icons/start_button.png',
                                    (window_size[1] // 3 + 10, window_size[1] // 3), window_size,
                                    (window_size[0] // 2, window_size[1] // 2 - 20), 'open_levels_menu')

        self._custom_player_button = Button(self._all_sprite, 'menu/icons/custom_player_button.png',
                                            (window_size[1] // 4, window_size[1] // 4), window_size,
                                            (window_size[0] // 4, window_size[1] // 2 - 10), '')

        self._create_levels_button = Button(self._all_sprite, 'menu/icons/create_levels_button.png',
                                            (window_size[1] // 4, window_size[1] // 4), window_size,
                                            (window_size[0] * 3 // 4, window_size[1] // 2 - 10), 'open_coming_soon')

        self._daily_button = Button(self._all_sprite, 'menu/icons/daily_button.png',
                                    (window_size[1] // 6, window_size[1] // 6), window_size,
                                    (window_size[0] * 14 // 15, window_size[1] // 2 - 10), '')

        self._more_games_button = Button(self._all_sprite, 'menu/icons/more_games_button.png',
                                         (window_size[1] // 5 + 20, window_size[1] // 5), window_size,
                                         (window_size[0] * 14 // 15, window_size[1] * 13 // 15), '')

        self._achievements_button = Button(self._all_sprite, 'menu/icons/achievements_button.png',
                                           (window_size[1] // 6, window_size[1] // 6), window_size,
                                           (window_size[0] * 5 // 15 + 30, window_size[1] * 13 // 15), '')

        self._settings_button = Button(self._all_sprite, 'menu/icons/settings_button.png',
                                       (window_size[1] // 6, window_size[1] // 6), window_size,
                                       (window_size[0] * 6.5 // 15 + 30, window_size[1] * 13 // 15), '')

        self._stats_button = Button(self._all_sprite, 'menu/icons/stats_button.png',
                                    (window_size[1] // 6, window_size[1] // 6), window_size,
                                    (window_size[0] * 8 // 15 + 30, window_size[1] * 13 // 15), '')

        self._newgrounds_button = Button(self._all_sprite, 'menu/icons/newgrounds_button.png',
                                         (window_size[1] // 6, window_size[1] // 6), window_size,
                                         (window_size[0] * 9.5 // 15 + 30, window_size[1] * 13 // 15), '')

        self._facebook_button = Button(self._all_sprite, 'menu/icons/facebook_button.png',
                                       (window_size[1] // 12, window_size[1] // 12), window_size,
                                       (window_size[0] // 20, window_size[1] * 16 // 20), '')

        self._x_button = Button(self._all_sprite, 'menu/icons/x_button.png',
                                (window_size[1] // 12, window_size[1] // 12), window_size,
                                (window_size[0] * 2 // 20, window_size[1] * 16 // 20), '')

        self._youtube_button = Button(self._all_sprite, 'menu/icons/youtube_button.png',
                                      (window_size[1] // 12, window_size[1] // 12), window_size,
                                      (window_size[0] * 3 // 20, window_size[1] * 16 // 20), '')

        self._twitch_button = Button(self._all_sprite, 'menu/icons/twitch_button.png',
                                     (window_size[1] // 12, window_size[1] // 12), window_size,
                                     (window_size[0] * 4 // 20, window_size[1] * 16 // 20), '')

        self._discord_button = Button(self._all_sprite, 'menu/icons/discord_button.png',
                                      (window_size[1] // 12, window_size[1] // 12), window_size,
                                      (window_size[0] * 4 // 20, window_size[1] * 18 // 20), '')

        self._exit_button = Button(self._all_sprite, 'menu/icons/exit_button.png',
                                   (window_size[1] // 10, window_size[1] // 10), window_size,
                                   (60, 60), 'open_exit_menu')

        self._exit_cancel_button = Button(self._exit_sprites, 'menu/icons/cancel_button.png',
                                          (int(window_size[0] / 5), int(window_size[1] / 7.5)), window_size,
                                          (window_size[0] * 4 // 10 + 40, window_size[1] * 6 // 10 + 12),
                                          'close_exit_menu')

        self._exit_yes_button = Button(self._exit_sprites, 'menu/icons/exit_yes_button.png',
                                       (int(window_size[0] / 7.5), int(window_size[1] / 7.5)), window_size,
                                       (window_size[0] * 6 // 10 - 10, window_size[1] * 6 // 10 + 12), 'exit')
        self._coming_soon = ComingSoon(self._scene, window_size)

        load_music('menu\sounds\menuLoop.mp3')
        pg.mixer.music.play(-1)

        self._event = ''
        self.init_ui()

    def init_ui(self) -> None:
        self._objects.extend([self._background, self._platforms, self._start_button, self._custom_player_button,
                              self._exit_button, self._create_levels_button, self._more_games_button,
                              self._daily_button, self._achievements_button, self._settings_button, self._stats_button,
                              self._newgrounds_button, self._facebook_button, self._x_button, self._youtube_button,
                              self._twitch_button, self._discord_button])
        self._exit_menu_buttons = [self._exit_cancel_button, self._exit_yes_button]
        for obj in self._objects:
            if isinstance(obj, Button):
                self._buttons.append(obj)

    def update(self) -> None:
        self._handle_event()
        for ob in self._objects:
            ob.update()
        MenuScene.color_background = (MenuScene.color_background + 1) if MenuScene.color_background <= 1529 else 0
        self._scene.fill(self.set_color(MenuScene.color_background))
        self._scene.blit(self._background, (0, 0))
        self._scene.blit(self._platforms, (0, self._window_size[1] - self._window_size[1] // 3))
        paste_image(self._scene, 'menu/icons/geometry_dash.png', (429 * 2.5, 50 * 2.5),
                    (self._window_size[0] // 2, self._window_size[1] // 5))
        paste_image(self._scene, 'menu/icons/robtop.png',
                    (self._window_size[0] * 3 // 20, self._window_size[1] * 2 // 20),
                    (self._window_size[0] * 4 // 40, self._window_size[1] * 18 // 20))
        self._all_sprite.draw(self._scene)
        if self._is_show_exit_menu:
            transparency = pg.Surface(self._window_size)
            transparency.set_alpha(180)
            self._scene.blit(transparency, (0, 0))
            paste_image(self._scene, 'menu/icons/exit_menu.png',
                        (self._window_size[0] // 2, self._window_size[1] // 2),
                        (self._window_size[0] // 2, self._window_size[1] // 2), color_key=(0, 0, 0))
            for button in self._exit_menu_buttons:
                button.update()
            self._exit_sprites.draw(self._scene)
        self._coming_soon.update()

    def _handle_event(self) -> None:
        self._event = ''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if not self._coming_soon.is_show:
                        self._event = 'open_exit_menu'
            elif event.type == pg.MOUSEBUTTONDOWN:
                lkm = 1
                if event.button == lkm:
                    buttons = self._buttons + self._exit_menu_buttons + [self._coming_soon]
                    for button in buttons:
                        if button.is_pressed:
                            self._event = button.signal
        if self._event == 'open_coming_soon':
            self._coming_soon.set_show(is_show=True, buttons=self._buttons + self._exit_menu_buttons)
            self._event = ''
        if self._event == 'close_coming_soon':
            self._coming_soon.set_show(is_show=False, buttons=self._buttons + self._exit_menu_buttons)
            self._event = ''
        if self._event == 'open_exit_menu':
            self.set_show_exit_menu(True)
            self._event = ''
        if self._event == 'close_exit_menu':
            self.set_show_exit_menu(False)
            self._event = ''
        if self._event == 'exit':
            sys.exit()

    def set_show_exit_menu(self, is_show: bool) -> None:
        self._is_show_exit_menu = is_show
        if self._is_show_exit_menu:
            MenuScene.set_lock(self._buttons, is_lock=True)
            MenuScene.set_lock(self._exit_menu_buttons, is_lock=False)
        else:
            MenuScene.set_lock(self._buttons, is_lock=False)
            MenuScene.set_lock(self._exit_menu_buttons, is_lock=True)

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

    @staticmethod
    def set_lock(buttons: list[Button], is_lock: bool):
        for button in buttons:
            button.set_lock(is_lock)
