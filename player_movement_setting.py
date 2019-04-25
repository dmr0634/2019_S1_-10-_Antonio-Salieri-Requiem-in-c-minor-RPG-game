import pygame
import os
from pygame.locals import *


class Player:

    def __int__(self, screen):
            self.screen = screen

            self.image = pygame.image.load(os.path.join('img', 'player.jpg'))

            self.x = 10
            self.y = 10

            self.width = self.image.get_width()
            self.height = self.image.get_height()

            self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[K_a]:
            self.x -= self.speed
        elif keys[K_d]:
            self.x += self.speed
        elif keys[K_w]:
            self.y -= self.speed
        elif keys[K_s]:
            self.y += self.speed

    def draw(self, screen = None):
        if screen is None:
            screen = self.screen

        screen.blit(self.image, (self.x, self.y))

