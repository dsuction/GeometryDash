import sys

import pygame as pg
from tools import load_image, load_music

class Button(pg.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = None


class Background(pg.Surface):
    def __init__(self, size):
        super().__init__(size)
        self.image = pg.transform.flip(pg.transform.scale(load_image('menu/icons/background.png'), size), True, True)
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.blit(self.image, (self.x, self.y))
        self.set_alpha(80)

    def update(self):
        self.x += 1
        self.blit(self.image, (self.x, self.y))


class MenuScene:
    def __init__(self, size):
        self._size = size
        self._scene = pg.Surface(size)
        self._scene.fill('blue')
        self.all_sprite = pg.sprite.Group()
        self.background = Background(size)
        self._scene.blit(self.background, (0, 0))
        load_music('menuLoop.mp3')
        pg.mixer.music.play(-1)

    def update(self):
        self.all_sprite.draw(self._scene)
        self.background.update()

    def handle_event(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()

    @property
    def scene(self):
        return self._scene


def menu_scene() -> pg.Surface:
    buttons_group_sprite = pg.sprite.Group()
    button_1 = Button(buttons_group_sprite)
    menu_screen = pg.Surface((100, 100))
    menu_screen.fill('red')
    return menu_screen
