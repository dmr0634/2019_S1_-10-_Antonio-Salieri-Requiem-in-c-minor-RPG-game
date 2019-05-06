'''
# dump: Since the game needs to be saved as readable text, all entity objects that need to be saved should be converted to data structures that json can express. (dict, list, str, int, float)
# load: Static method, returning a type instance from json data, since Game is a global singleton pattern, the load function changes itself.
'''

import json
import pygame as pg
from utils import openres, relpath


class Game:

    " Control game save, load, run, interface switch, and clock cycle"
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.timer = pg.time.Clock()
        self.fps = 60
        self.msg = ''

    " Definition load function by using .json file"
    def load(self, fn):
        with open(relpath(fn), 'r') as file:
            data = json.load(file)
        self.player = Player.load(data['player'])
        self.level = Level.load(data['level'])

    " Definition save function through using .json file"
    " Variable as player and level"
    def save(self, fn):
        json.dump\
        ({
            'player': self.player.to_data(),
            'level': self.level.name
        }, open(relpath(fn), 'w'))

    " Start interface"
    def run(self):
        from scene import Start
        self.secen = Start()
        while True:

            " Elapse: time interval (ms)"
            elapse = self.timer.tick(self.fps)

            " Execution interface logic"
            self.secen.run(elapse)

            " Screen render"
            self.secen.render(self.screen)

            " Refresh screen"
            pg.display.flip()


game = Game()


class Player:

    " Player img reading"
    frames = {
        dir: openres(f'images/player/{dir}.png').convert_alpha()
        for dir in ['up', 'down', 'left', 'right']
    }

    " Python custom constructor, the initial variable defined by itself."
    " Based on python is a dynamic language, so renew variable without need to redefine it again."
    def __init__(self, dir, rect, speed, health, exp, attack, items):
        self.dir = dir
        self.exp = exp
        self.rect = rect # pygame.Rect
        self.speed = speed
        self.health = health
        self.attack = attack
        self.items = items # set

    def run(self, elapse):
        rect = self.rect.copy()
        keys = pg.key.get_pressed()

        " Control method"
        if keys[pg.K_LEFT]:
            rect.x -= self.speed
            self.dir = 'left'
        elif keys[pg.K_RIGHT]:
            rect.x += self.speed
            self.dir = 'right'
        elif keys[pg.K_UP]:
            rect.y -= self.speed
            self.dir = 'up'
        elif keys[pg.K_DOWN]:
            rect.y += self.speed
            self.dir = 'down'

        " Renew the coordinates without conflict with the map"
        if not game.level.check_collide(rect):
            self.rect = rect

    " Screen rendering (print out the window)"
    def render(self, screen):
        screen.blit(self.frames[self.dir], self.rect)

    " Rect the type of PyGame.Rect and Items are of type set (line 71 and 75)"
    " Since the game needs to be saved as readable text, all entity objects that need to be saved should be available. Data structure that can be expressed by conversion to json"
    " This two method is for converted into a data structure that json can express"
    def to_data(self):
        data = self.__dict__.copy()
        data['rect'] = list(self.rect)
        data['items'] = list(self.items)
        return data

    @staticmethod
    def load(data):
        data['rect'] = pg.Rect(data['rect'])
        data['items'] = set(data['items'])
        return Player(**data)

    " '__str__' is the method to call when converting a type to a string"
    " Change .json type structure into character then printout"
    def __str__(self):
        return f'Speed: {self.speed}    Health: {self.health}    Attack: {self.attack}    EXP: {self.exp}'


class Enemy:

    " Enemy data"
    img = openres('images/enemy/goast.png').convert_alpha()
    exp = 10
    attack = 10
    health = 100
    name = 'Ghost'


class Key(pg.Rect):

    " Keys img"
    img = openres('images/key.png')

    " '__*__'' function is a type of python's function"
    def __init__(self, pos, id):
        rect = self.img.get_rect()
        rect.center = pos
        super().__init__(rect)
        self.id = id

    " Data reconstruction is used to cater to .json"
    " Don't have to return the .json format then can do it without conflicts"
    " For game load and save"
    def __hash__(self):
        return self.id.__hash__()

class Portal(pg.Rect):

    " Path reload position (The point to the next area)"
    def __init__(self, rect, id, level, pos, key):
        super().__init__(rect)
        self.id = id
        self.level = level
        self.pos = pos
        self.key = key

" The hold class for the hold level logic"
class Level:

    " identify the variable using in the level"
    def __init__(self, name, portals, bg):
        self.name = name
        self.portals = portals
        self.keys = set()
        self.bg = bg

    @staticmethod
    def load(n):

        " Different levels, the initialization file is not the same, 'n' means the first few levels, 'openres' is to load the corresponding configuration file, and step as initialize"
        portals = openres(f'levels/{n}/portals.json')
        portals = [Portal(**p) for p in portals]
        bg = openres(f'levels/{n}/background.jpg')
        return Level(n, portals, bg.convert())

    def render(self, screen):
        screen.blit(self.bg, (0, 0))
        for key in self.keys:
            screen.blit(key.img, key)

    def run(self, elapse):
        self.check_portal()
        self.check_key()

    " Check the player have key or not"
    def check_portal(self):
        i = game.player.rect.collidelist(self.portals)
        if i == -1: return

        " Key's position"
        portal = self.portals[i]
        if portal.key not in game.player.items:
            game.msg = f'You need the key of {portal.id}.'
            key = Key((100, 100), portal.key)
            game.level.keys.add(key)
            return

        game.level = Level.load(portal.level)
        game.player.rect.center = portal.pos

    " Get key to next area, this method is for determine if the player has a key or not."
    def check_key(self):
        keys = list(self.keys)
        i = game.player.rect.collidelist(keys)
        if i != -1:
            key = keys[i]
            self.keys.remove(key)
            game.player.items.add(key.id)

    def check_collide(self, rect):

        " Check for conflicts in the current scene"
        return self.bg.get_rect().contains(rect) == 0
