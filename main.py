import pygame as pg

from scenes.menu.scene_menu import MenuScene
from scenes.levels_menu.scene_levels_menu import LevelsMenuScene
from scenes.scene import Scene
from scenes.levels.level_scene import LevelScene

FPS = 60


def main():
    pg.init()
    screen = pg.display.set_mode(flags=pg.FULLSCREEN | pg.DOUBLEBUF)
    window_size = screen.get_size()
    clock = pg.time.Clock()
    scene: Scene = MenuScene(window_size)

    while True:
        scene.update()
        if scene.event == 'open_levels_menu':
            scene: Scene = LevelsMenuScene(window_size)
        elif scene.event == 'return_to_menu':
            scene: Scene = MenuScene(window_size)
        elif 'open_level' in scene.event:
            scene: Scene = LevelScene(scene.event.replace('open_level', ''), window_size)
        elif scene.event == 'return_to_levels_menu':
            scene: Scene = LevelsMenuScene(window_size)
        screen.blit(scene.scene, (0, 0))
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
