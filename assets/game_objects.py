from tokenize import group

import pygame as pg
from utils.utils import  load_image
from abc import ABC, abstractmethod


class GameObject(ABC):
    @abstractmethod
    def update(self):
        pass


class Button(pg.sprite.Sprite, GameObject):
    def __init__(self, group: pg.sprite.Group, path_image: str, size: tuple[int, int], size_window: tuple[int, int],
                 pos: tuple[int, int], signal: str) -> None:
        super().__init__(group)
        self._pos = pos
        self._size = size
        self._size_window = size_window
        self._signal = signal
        self._is_pressed = False
        self._is_lock = False
        increase = 1.2
        self._image_1 = pg.transform.scale(load_image(path_image), size)
        self._image_2 = pg.transform.scale(load_image(path_image), (size[0] * increase, size[1] * increase))
        self.image = self._image_1
        self.rect = self.image.get_rect()
        self.update()

    def set_lock(self, is_lock: bool) -> None:
        self._is_lock = is_lock

    def update(self) -> None:
        if self.check_mouse_pos(self.rect) and not self._is_lock:
            self.image = self._image_2
        else:
            self.image = self._image_1
        self.rect = self.image.get_rect()
        self.rect.x = self._pos[0] - self.rect.w // 2
        self.rect.y = self._pos[1] - self.rect.h // 2

    @staticmethod
    def check_mouse_pos(rect: pg.Rect) -> bool:
        mouse_pos = pg.mouse.get_pos()
        if rect.x <= mouse_pos[0] <= rect.x + rect.w and rect.y <= mouse_pos[1] <= rect.y + rect.h:
            return True
        return False

    @property
    def is_pressed(self) -> bool:
        mouse_pressed = pg.mouse.get_pressed()
        if self.check_mouse_pos(self.rect) and mouse_pressed[0]:
            self._is_pressed = True
        else:
            self._is_pressed = False
        return self._is_pressed

    @property
    def signal(self) -> str:
        if self._is_lock:
            return ''
        return self._signal


class Background(pg.Surface, GameObject):
    def __init__(self, windows_size: tuple[int, int], path_image: str) -> None:
        super().__init__((windows_size[0], windows_size[1] - windows_size[1] // 3))
        self.image = pg.transform.flip(pg.transform.scale(load_image(path_image), windows_size), True, True)
        self._x1 = 0
        self._x2 = self.image.get_width()
        self._y = 0
        self._speed = 2
        transparency = 100
        self.set_alpha(transparency)

    def update(self) -> None:
        self._x1 -= self._speed
        self._x2 -= self._speed
        if self._x1 <= -self.image.get_width():
            self._x1 = self._x2
            self._x2 = self.image.get_width()
        self.blit(self.image, (self._x1, self._y))
        self.blit(self.image, (self._x2, self._y))


class Platform(pg.sprite.Sprite, GameObject):
    count_platform = 0
    def __init__(self, image_path: str, window_size: tuple[int, int], speed: int,  *group):
        super().__init__(*group)
        self._speed = speed
        self._side_size = window_size[1] // 3
        self._window_size = window_size
        self.image = pg.transform.scale(load_image(image_path), (self._side_size, self._side_size))
        self.rect = self.image.get_rect()
        self.rect.x = self._side_size * Platform.count_platform
        self.rect.y = 0
        self.mask = pg.mask.from_surface(self.image)
        Platform.count_platform += 1

    def update(self):
        if self.rect.x + self.rect.w <= 0:
            self.rect.x = self._side_size * (Platform.count_platform - 1)
        self.rect.x -= self._speed

    @property
    def side_size(self):
        return self._side_size


class Platforms(pg.Surface, GameObject):
    def __init__(self, window_size: tuple[int, int]):
        self._size  = (window_size[0], window_size[1] // 3)
        super().__init__(self._size)
        Platform.count_platform = 0
        self.set_colorkey('black')
        transparency = 110
        self.set_alpha(transparency)
        self._platforms_group = pg.sprite.Group()
        self._quantity = window_size[0] // (window_size[1] // 3) + 2
        self._platforms = []
        for i in range(self._quantity):
            self._platforms.append(Platform('menu/icons/platform.png', window_size, 15,
                                            self._platforms_group))

    def update(self) -> None:
        self._platforms_group.update()
        self._platforms_group.draw(self)

    @property
    def platform_group(self) -> pg.sprite.Group:
        return self._platforms_group


class Block(GameObject, pg.sprite.Sprite):
    path_image = 'menu/icons/x_button.png'

    def __init__(self, groups: pg.sprite.Group, pos: tuple[int, int], speed: int) -> None:
        super().__init__(groups)
        self._speed = speed
        self.image: pg.Surface = load_image(self.path_image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def update(self) -> None:
        self.rect.x -= self._speed


class Spike(GameObject, pg.sprite.Sprite):
    path_image = 'menu/icons/x_button.png'

    def __init__(self, groups: pg.sprite.Group, pos: tuple[int, int], speed: int) -> None:
        super().__init__(groups)
        self._speed = speed
        self.image: pg.Surface = load_image(self.path_image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def update(self) -> None:
        self.rect.x -= self._speed


class Wall(GameObject, pg.sprite.Sprite):
    path_image = 'menu/icons/x_button.png'
    
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image(self.path_image)

    def update(self):
        pass
