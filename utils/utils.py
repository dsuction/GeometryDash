import os
import sys
import pygame as pg
import json


def check_file(path: str) -> str:
    fullname = os.path.join('assets', path)
    if not os.path.isfile(fullname):
        print(f'Error: file not found \'{fullname}\'')
        sys.exit()
    return fullname


def load_image(path: str, color_key=None) -> pg.Surface:
    fullname: str = check_file(path)
    image: pg.Surface = pg.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image: pg.Surface = image.convert_alpha()
    return image


def load_music(path: str) -> None:
    fullname: str = check_file(path)
    pg.mixer.music.load(fullname)


def load_sound(path: str) -> pg.mixer.Sound:
    fullname: str = check_file(path)
    return pg.mixer.Sound(fullname)


def paste_image(scene: pg.Surface, path_image: str, size_image: tuple[int, int], pos: tuple[int, int],
                color_key=None) -> None:
    image: pg.Surface = pg.transform.scale(load_image(path_image, color_key=color_key), size_image)
    scene.blit(image, (pos[0] - size_image[0] // 2, pos[1] - size_image[1] // 2))


def load_json(path: str) -> dict:
    fullname: str = check_file(path)
    with open(fullname, 'r') as f:
        level = json.load(f)
    return level


def save_json(path: str, data: dict):
    fullname: str = check_file(path)
    with open(fullname, 'w') as f:
        json.dump(data, f)


def get_names_files_directory(path: str) -> list[str]:
    fullname: str = os.path.join('assets', path)
    if not os.path.isdir(fullname):
        sys.exit()
    files = os.listdir(fullname)
    files = [i for i in files if 'icons' not in i]
    return files
