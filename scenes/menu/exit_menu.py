import pygame as pg


from scenes.scene import Scene
from scenes.menu.scene_menu import MenuScene

class ExitMenu(Scene):
    def __init__(self, window_size: tuple[int, int]):
        super().__init__(window_size)
        self._buttons: list[Button] =  []
        self._all_sprite = pg.sprite.Group()
