import pygame as pg


def main():
    FPS = 60
    pg.init()
    clock = pg.time.Clock()
    while True:
        clock.tick(FPS)


if __name__ == '__main__':
    main()
