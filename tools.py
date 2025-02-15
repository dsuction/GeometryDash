import os
import sys
import pygame as pg


def load_image(path: str, color_key=None) -> pg.Surface:
    fullname = os.path.join('Assets', path)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pg.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_music(path: str):
    fullname = os.path.join('Assets', path)
    if not os.path.isfile(fullname):
        sys.exit()
    return pg.mixer.music.load(fullname)