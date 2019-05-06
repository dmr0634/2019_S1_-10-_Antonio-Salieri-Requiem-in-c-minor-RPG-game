RESOLUTION = 800, 600

import pygame as pg
import pygame

pygame.mixer.init()
pygame.init()

pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(0.5) #0.1 - 1
pygame.mixer.music.play(-1) #-1 means play the music again and agian
pg.init()
screen = pg.display.set_mode(RESOLUTION)
pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

from entity import game

game.run()
