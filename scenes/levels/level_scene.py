import sys
import pygame as pg

from scenes.scene import Scene
from utils.utils import load_level
from assets.game_objects import Spike, Block, Background, Platforms
from player import Player


class LevelScene(Scene):
    def __init__(self, path_level: str, window_size: tuple[int, int]) -> None:
        super().__init__(window_size)
        path_level = 'levels/' + path_level
        self._color: list[int] = [0, 0, 0]
        self._damage_objects_group = pg.sprite.Group()
        self._player_group = pg.sprite.Group()
        self._blocks_group = pg.sprite.Group()
        self._background = Background(window_size, 'menu/icons/background.png')
        self._platforms = Platforms(window_size)
        self._player = Player((100, 0), self._blocks_group, self._damage_objects_group, window_size, self._player_group)
        self._level: dict = load_level(path_level)
        self._speed = 15
        self._x = 0
        self.init_ui()

    def init_ui(self) -> None:
        for obj in self._level['objects']:
            if obj[0] == 'spike':
                Spike(self._damage_objects_group, (obj[1][0], -obj[1][1] + self._window_size[1] * 2 // 3 - 50), self._speed)
            elif obj[0] == 'block':
                Block(self._blocks_group, (obj[1][0], -obj[1][1] + self._window_size[1] * 2 // 3 - 50), self._speed)

    def update(self) -> None:
        self._scene.fill(self._color)
        self._background.update()
        self._platforms.update()
        self._player_group.update()
        self._scene.blit(self._background, (0, 0))
        self._scene.blit(self._platforms, (0, self._window_size[1] - self._window_size[1] // 3))
        self._handle_event()

        self._damage_objects_group.draw(self._scene)
        self._blocks_group.draw(self._scene)
        self._player_group.draw(self._scene)

        self._damage_objects_group.update()
        self._blocks_group.update()

        self._x += self._speed

        for obj in self._level['objects']:
            if obj[0] == 'color':
                if obj[2] <= self._x:
                    self._color = obj[1]

    def _handle_event(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self._event = 'return_to_levels_menu'
