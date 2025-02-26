import pygame as pg
from utils.utils import load_image, load_level


class Player(pg.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], blocks_group, damage_group, window_size, *groups):
        super().__init__(*groups)
        self._window_size = window_size
        self._angle = 0
        self._blocks_group = blocks_group
        self._damage_group = damage_group
        self._original_image: pg.Surface = load_image(load_level('player/settings/player.json')['path_image'])
        self.image = self._original_image
        self.rect = self.image.get_rect(center=pos)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        if not pg.sprite.spritecollideany(self, self._blocks_group) and self.rect.y + self.rect.h < self._window_size[1] * 2 // 3:
            self.rect.y += 10
        self.rotate()

    def rotate(self):
        self._angle += 5
        self.image = pg.transform.rotate(self._original_image, self._angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pg.mask.from_surface(self.image)
