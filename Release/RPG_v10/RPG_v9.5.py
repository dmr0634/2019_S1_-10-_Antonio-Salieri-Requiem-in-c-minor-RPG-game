import pygame as pg

from const import RESOLUTION

if __name__ == "__main__":

    pg.init()
    pg.display.set_mode(RESOLUTION)

    pg.mixer.music.load('bgm.mp3')
    pg.mixer.music.set_volume(0.5)
    pg.mixer.music.play(-1)

    from scene import SceneM
    SceneM().run()
