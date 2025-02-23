import pygame
import pygame as pg

from tools.choice_scene import choice_scene
from scenes.menu.scene_menu import MenuScene
from scenes.scene import Scene
FPS = 60


def main():
    pg.init()
    screen = pg.display.set_mode(flags=pg.FULLSCREEN)
    size = screen.get_size()
    clock = pg.time.Clock()
    scene: Scene = MenuScene(size)
    while True:
        scene.update()
        scene: Scene  = choice_scene[scene.event](size) if scene.event else scene
        screen.blit(scene.scene, (0, 0))
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
