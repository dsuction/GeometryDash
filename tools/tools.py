import os
import sys
import pygame as pg


def load_image(path: str, color_key=None) -> pg.Surface:
    fullname = os.path.join('assets', path)
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
    fullname = os.path.join('assets', path)
    if not os.path.isfile(fullname):
        sys.exit()
    return pg.mixer.music.load(fullname)


def paste_image(scene: pg.Surface, path_image: str, size_image: tuple[int, int], pos: tuple[int, int], color_key=None) -> None:
    image = pg.transform.scale(load_image(path_image, color_key=color_key), size_image)
    scene.blit(image, (pos[0] - size_image[0] // 2, pos[1] - size_image[1] // 2))
