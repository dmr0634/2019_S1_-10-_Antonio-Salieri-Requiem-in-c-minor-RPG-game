import os
import random
from datetime import datetime

import pygame as pg

from entity import game, Level, Enemy
from utils import openres, relpath

" This class is mainly used to set the GUI's composing, message bar's font and word's type"
class Scene:

    " Construction parameter"
    def __init__(self, prev):
        self.prev = prev

    " Set key's even"
    def run(self, elapse):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return self.exit()
            elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                return self.back()

        self.update(elapse)

    " Interface custom logic"
    def update(self, elapse):
        pass

    def exit(self):
        pg.quit()
        exit()

    " If not per interface then return to start interface"
    def back(self):
        game.secen = self.prev or Start()


class Main(Scene):

    " Main interface"
    def __init__(self, prev=None):
        menu = Menu(self)
        super().__init__(menu)

    def update(self, elapse):
        game.player.run(elapse)
        game.level.run(elapse)
        self.random_combat()

    " Probability of encountering an enemy"
    " Then trigger the battle GUI"
    def random_combat(self):
        if random.random() < 0.001:
            game.secen = Combat(self)

    " Rendering of the battle GUI"
    def render(self, screen):
        screen.fill((255, 255, 255))
        game.level.render(screen)
        game.player.render(screen)
        prop = str(game.player)

        " Message bar format and size"
        prop = pg.font.Font(None, 32).render(prop, True, (128, 128, 128))
        msg = pg.font.Font(None, 24).render(game.msg, True, (128, 128, 128))

        " Then built(past) it in the screen"
        screen.blit(msg, (0, 520))
        screen.blit(prop, (0, 580))


class Combat(Scene):
    font = pg.font.Font(None, 42)

    " Battle GUI"
    def __init__(self, prev):
        super().__init__(prev)
        self.enemy = Enemy()
        self.option = 0
        self.skills = [('Attack', self.attack), ('Run Away', self.escape)]

    " There are two options when the battle occurs."
    " Run and Attack"
    def run(self, elapse):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return self.exit()
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    return self.skills[self.option][1]()
                elif e.key == pg.K_DOWN:
                    self.option += 1
                elif e.key == pg.K_UP:
                    self.option -= 1
                self.option %= len(self.skills)

    def attack(self):
        self.enemy.health -= game.player.attack
        if self.enemy.health <= 0:
            game.player.exp += self.enemy.exp
            game.msg = f'You defeated {self.enemy.name}!'
            return self.back()

        game.player.health -= self.enemy.attack
        if game.player.health <= 0:
            game.secen = Gameover(None)

    " Message bar for escaped"
    def escape(self):
        game.msg = 'You escaped.'
        game.secen = self.prev

    def render(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.enemy.img, (190, 100))
        for i, (skill, _) in enumerate(self.skills):
            color = (0, 0, 0) if i == self.option else (128, 128, 128)
            skill = self.font.render(skill, True, color)
            screen.blit(skill, (550, 300 + i * 50))
        prop = str(game.player)
        prop = pg.font.Font(None, 32).render(prop, True, (128, 128, 128))
        msg = pg.font.Font(None, 24).render(game.msg, True, (128, 128, 128))
        screen.blit(msg, (0, 520))
        screen.blit(prop, (0, 580))


class Help(Scene):
    def run(self, elapse):
        if pg.event.get(pg.KEYDOWN):
            return self.back()

    def render(self, screen):
        help = openres('images/help.png')
        screen.blit(help, (0, 0))


class Gameover(Scene):
    font = pg.font.Font(None, 42)

    def render(self, screen):
        screen.fill((0, 0, 0))
        gameover = self.font.render('Gameover', True, (255, 255, 255))
        screen.blit(gameover, (280, 250))


class MenuBase(Scene):
    font = pg.font.Font(None, 42)
    menus = []
    option = 0

    def move(self, i):
        self.option = (self.option + i) % len(self.menus)

    def enter(self):
        return self.menus[self.option][1]()

    "Key's event"
    def run(self, elapse):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return self.enter()
                elif event.key == pg.K_DOWN:
                    self.move(1)
                elif event.key == pg.K_UP:
                    self.move(-1)
                elif event.key == pg.K_ESCAPE:
                    return self.back()
        return self

    "Step up interface and rendering"
    def render(self, screen):

        " Step as full screen"
        screen.fill((0, 0, 0))
        for i, (menu, _) in enumerate(self.menus):
            color = (255, 255, 255) if i == self.option else (128, 128, 128)
            menu = self.font.render(menu, True, color)
            screen.blit(menu, (54, 54 * i + 54))

" Menu bar option link to function"
class Menu(MenuBase):
    def __init__(self, prev):
        super().__init__(prev)
        self.menus = [('Continue', self.back), ('Save Game', self.save_game),
                      ('Start Menu', self.start_menu), ('Exit', self.exit)]

    def start_menu(self):
        game.secen = Start()

    " Date and time types"
    " Path for saving file"
    def save_game(self):
        dt = str(datetime.now()).replace(':', '-')
        fn = relpath(f'saves/{dt}.txt')
        game.save(fn)


class Start(MenuBase):
    def __init__(self, prev=None):
        super().__init__(prev)
        self.menus = [('New Game', self.new_game), ('Load Game',self.load_game),('Exit', self.exit)]

    def new_game(self):
        game.load('init.json')
        game.secen = Help(Main())

    def load_game(self):
        game.secen = Load(self)


class Load(MenuBase):
    def __init__(self, prev):
        super().__init__(prev)

        def load(fn):
            fn = 'saves/' + fn

            def func():
                game.load(fn)
                game.secen = Main()

            return func

        self.menus = [(fn, load(fn)) for fn in sorted(os.listdir('saves'), reverse=True)]
