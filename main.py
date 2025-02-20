import pygame
import pygame as pg
from scenes.menu.scene_menu import MenuScene
from scenes.levels_menu.scene_levels_menu import LevelsMenuScene
FPS = 60


def main():
    pg.init()
    screen = pg.display.set_mode(flags=pygame.FULLSCREEN)
    size = screen.get_size()
    clock = pg.time.Clock()
    scene = MenuScene(screen.get_size())
    while True:
        scene.update()
        if scene.event == 'open_levels_menu':
            scene = LevelsMenuScene(size)
        elif scene.event == 'return_to_menu':
            scene = MenuScene(size)
        screen.blit(scene.scene, (0, 0))
        clock.tick(FPS)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
