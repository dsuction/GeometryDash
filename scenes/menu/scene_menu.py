import sys
from importlib.metadata import pass_none

import pygame as pg
from tools import load_image, load_music


class Button(pg.sprite.Sprite):
    def __init__(self, group, image, size, size_window):
        super().__init__(group)
        self.size = size
        self.size_window = size_window
        self.image = pg.transform.scale(load_image(image), size)
        self.rect = self.image.get_rect()
        self.rect.x = size_window[0] // 2 - self.rect.w // 2
        self.rect.y = size_window[1] // 2 - self.rect.h // 2

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.x <= mouse_pos[0] <= self.rect.x + self.rect.w and self.rect.y <= mouse_pos[1] <= self.rect.y + self.rect.h:
            self.image = pg.transform.scale(self.image, (self.size[0] * 1.2, self.size[1] * 1.2))
        else:
            self.image = pg.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = self.size_window[0] // 2 - self.rect.w // 2
        self.rect.y = self.size_window[1] // 2 - self.rect.h // 2


class Text(pg.Surface):
    def __init__(self, image, size, size_window):
        super().__init__(size)
        self.size = size
        self.image = pg.transform.scale(load_image(image), size)
        self.blit(self.image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = size_window[0] // 2 - self.rect.w // 2
        self.rect.y = size_window[1] // 2 - self.rect.h // 2


class Background(pg.Surface):
    def __init__(self, size):
        super().__init__((size[0], size[1] - size[1] // 3))
        self.image = pg.transform.flip(pg.transform.scale(load_image('menu/icons/background.png'), size), True, True)
        self.x_1 = 0
        self.x_2 = self.image.get_width()
        self.y = 0
        self.speed = 2
        self.set_alpha(100)

    def update(self):
        self.x_1 -= self.speed
        self.x_2 -= self.speed
        if self.x_1 <= -self.image.get_width():
            self.x_1 = self.x_2
            self.x_2 = self.image.get_width()
        self.blit(self.image, (self.x_1, self.y))
        self.blit(self.image, (self.x_2, self.y))


class Platform(pg.Surface):
    def __init__(self, size):
        self.side_size = size[1] // 3
        self.quantity = size[0] // self.side_size + 2
        super().__init__((size[0], self.side_size))
        self.image = pg.transform.scale(load_image('menu/icons/platform.png'), (self.side_size, self.side_size))
        self.speed = 15
        self.y = 0
        self.x = [self.side_size * i for i in range(self.quantity)]
        for x in self.x:
            self.blit(self.image, (x, 0))
        self.set_alpha(55)

    def update(self):
        self.fill('black')
        for i in range(self.quantity):
            self.x[i] -= self.speed
            if self.x[i] < -self.side_size:
                self.x.pop(0)
                self.x.append(self.x[-1] + self.side_size)
        for x in self.x:
            self.blit(self.image, (x, self.y))


class MenuScene:
    def __init__(self, size):
        self._size = size
        self._scene = pg.Surface(size)
        self._scene.fill('blue')
        self.all_sprite = pg.sprite.Group()
        self.background = Background(size)
        self.platforms = Platform(size)
        self.start_button = Button(self.all_sprite, 'menu/icons/start_button.png', (size[1] // 3, size[1] // 3), size)
        self.geometry_dash = load_image('menu/icons/geometry_dash.png')
        load_music('menuLoop.mp3')
        pg.mixer.music.play(-1)
        self.color = 0

    def update(self):
        self.handle_event()
        self.background.update()
        self.platforms.update()
        self.start_button.update()
        self.color = (self.color + 1) if self.color <= 1529 else 0
        self._scene.fill(self.color_(self.color))
        self._scene.blit(self.background, (0, 0))
        self._scene.blit(self.platforms, (0, self._size[1] - self._size[1] // 3))
        self._scene.blit(self.geometry_dash, (200, 100))
        self.all_sprite.draw(self._scene)

    @staticmethod
    def color_(color: int) -> pg.color:
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

    def handle_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()

    @property
    def scene(self):
        return self._scene
