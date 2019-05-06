import sys

import pygame

from core import Sprite,GameMap, CharWalk


class Game:
    def __init__(self, title, width, height, fps=60):
        """
        :param title: windows's title
        :param width: windows's width
        :param height: window's height
        :param fps: game refresh speed per second
        """
        self.title = title
        self.width = width
        self.height = height
        self.screen_surf = None
        self.fps = fps
        self.__init_pygame()
        self.__init_game()
        self.update()

    def __init_pygame(self):
        """
        pygame initialization event
        """
        pygame.init()
        pygame.display.set_caption(self.title)
        self.screen_surf = pygame.display.set_mode([self.width, self.height])
        self.clock = pygame.time.Clock()

    def __init_game(self):
        """
        game initialization event
        """
        self.hero = pygame.image.load('./img/character/hero.png').convert_alpha()
        self.map_bottom = pygame.image.load('./img/map/0.png').convert_alpha()
        self.map_top = pygame.image.load('./img/map/0_top.png').convert_alpha()
        self.game_map = GameMap(self.map_bottom, self.map_top, 0, 0)
        self.game_map.load_walk_file('./img/map/0.map')
        self.role = CharWalk(self.hero, 48, CharWalk.DIR_DOWN, 5, 10)

    def update(self):
        while True:
            self.clock.tick(self.fps)
            # update logic
            self.role.logic()
            self.event_handler()
            self.game_map.roll(self.role.x, self.role.y)
            # update  display
            self.game_map.draw_bottom(self.screen_surf)
            self.role.draw(self.screen_surf, self.game_map.x, self.game_map.y)
            self.game_map.draw_top(self.screen_surf)
            # self.game_map.draw_grid(self.screen_surf)
            pygame.display.update()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mx = int((mouse_x - self.game_map.x) / 32)
                my = int((mouse_y - self.game_map.y) / 32)
                self.role.find_path(self.game_map, (mx, my))


if __name__ == '__main__':
    Game("Antonio Salieri: Requiem in c minor", 640, 480)