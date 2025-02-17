import pygame
import pygame as pg
from scenes.menu.scene_menu import MenuScene

FPS = 60


def main():
    size = width, height = 500, 500
    pg.init()
    screen = pg.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pg.time.Clock()
    scene = MenuScene(screen.get_size())
    is_running = True
    pg.mixer.music.load('Assets/menuLoop.mp3')
    pg.mixer.music.play(-1)
    while is_running:
        scene.update()
        screen.blit(scene.scene, (0, 0))
        clock.tick(FPS)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
