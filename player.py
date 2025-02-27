import sys

import pygame as pg
from utils.utils import load_image, load_json


class Player(pg.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], blocks_group: pg.sprite.Group, damage_group: pg.sprite.Group, window_size: tuple[int, int], *groups):
        super().__init__(*groups)
        self._window_size = window_size
        self._angle = 0
        self._velocity_y = 10
        self._is_play = True
        self._jump = False
        self._blocks_group = blocks_group
        self._damage_group = damage_group
        self._original_image: pg.Surface = pg.transform.scale(load_image(load_json('player/settings/player.json')['path_image']), (100, 100))
        self._shadow = pg.sprite.Sprite()
        self._shadow.rect = self._original_image.get_rect(center=pos)
        self.image = self._original_image
        self.rect = self.image.get_rect(center=pos)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        if not pg.sprite.spritecollideany(self._shadow, self._blocks_group) and self._shadow.rect.y + self._shadow.rect.h < self._window_size[1] * 2 // 3:
            self._velocity_y += 20
            if self._velocity_y == 0:
                self._velocity_y = 1
            self.rect.y += (self._velocity_y / 60)
            self._shadow.rect.y += (self._velocity_y / 60)
            self.rotate()
        else:
            if self._angle % 90 != 0:
                self.rotate()
            else:
                self._velocity_y = 0
        if any(pg.mouse.get_pressed(num_buttons=5)) and self._velocity_y == 0:
            self._velocity_y = -700
            self.rect.y -= 5
            self._shadow.rect.y -= 5
        if pg.sprite.spritecollideany(self, self._damage_group):
            self._is_play = False

    def rotate(self):
        self._angle -= 10
        self.image = pg.transform.rotate(self._original_image, self._angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pg.mask.from_surface(self.image)

    @property
    def is_play(self):
        return self._is_play
