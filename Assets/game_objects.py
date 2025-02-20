import pygame as pg
from tools import  load_image
from abc import ABC, abstractmethod


class GameObject(ABC):
    @abstractmethod
    def update(self):
        pass


class Button(pg.sprite.Sprite, GameObject):
    def __init__(self, group: pg.sprite.Group, path_image: str, size: tuple[int, int], size_window: tuple[int, int],  pos: tuple[int, int], signal: str) -> None:
        super().__init__(group)
        self._pos = pos
        self._size = size
        self._size_window = size_window
        self._signal = signal
        self._is_pressed = False
        increase = 1.2
        self._image_1 = pg.transform.scale(load_image(path_image), size)
        self._image_2 = pg.transform.scale(load_image(path_image), (size[0] * increase, size[1] * increase))
        self.image = self._image_1
        self.rect = self.image.get_rect()
        self.update()

    def update(self) -> None:
        if self.check_mouse_pos(self.rect):
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
        return self._signal


class Background(pg.Surface, GameObject):
    def __init__(self, windows_size, image) -> None:
        super().__init__((windows_size[0], windows_size[1] - windows_size[1] // 3))
        self.image = pg.transform.flip(pg.transform.scale(load_image(image), windows_size), True, True)
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
    def __init__(self, image_path: str, window_size: tuple[int, int], speed: int=15, *grop):
        super().__init__(*grop)
        self.image = load_image(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        # self._image = load_image(image_path)
        # self._side_size = self._image.get_size()[0]
        # self._quantity = window_size[0] // self._side_size + 2
        # super().__init__((window_size[0], self._side_size))
        # self._speed = speed
        # self.y = 0
        # self.all_x = [self._side_size * i for i in range(self._quantity)]
        # for x in self.all_x:
        #     self.blit(self._image, (x, 0))
        # transparency = 55
        # self.set_alpha(transparency)

    def update(self):
        pass
        # self.fill('black')
        # for i in range(self._quantity):
        #     self.all_x[i] -= self._speed
        #     if self.all_x[i] < -self._side_size:
        #         self.all_x.pop(0)
        #         self.all_x.append(self.all_x[-1] + self._side_size)
        # for x in self.all_x:
        #     self.blit(self._image, (x, self.y))

    @property
    def side_size(self):
        return self._side_size


class Platforms(GameObject):
    pass
