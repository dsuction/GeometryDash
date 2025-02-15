import pygame
import pygame as pg
from scenes.menu.scene_menu import MenuScene

FPS = 60


def main():
    size = width, height = 500, 500
    pg.init()
    screen = pg.display.set_mode((0, 0), pygame.FULLSCREEN)
    size = screen.get_size()
    clock = pg.time.Clock()
    scene = MenuScene(size)
    is_running = True
    pg.mixer.music.load('Assets/menuLoop.mp3')
    pg.mixer.music.play(-1)
    while is_running:
        scene.update()
        screen.blit(scene.scene, (0, 0))
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    is_running = False
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
