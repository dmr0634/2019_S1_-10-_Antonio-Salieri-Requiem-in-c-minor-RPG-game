import unittest
from unittest.mock import MagicMock, patch
RESOLUTION = 800, 600

import pygame as pg

pg.init()
screen = pg.display.set_mode(RESOLUTION)
pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])
from scene import MenuBase, Scene, Combat, Start
from entity import game, Player


def test_func():
    return 1


def test_func2():
    return 2


def test_func3():
    return 3


def create_key_mock(pressed_key):
    def helper():
        tmp = [0] * 300
        tmp[pressed_key] = 1
        return tmp
    return helper()


class TestGameFunction(unittest.TestCase):

    def setUp(self):
        self.menu = MenuBase(Scene)
        self.combat = Combat(Scene)
        self.player = Player('images/players/down.png', [100, 120], 5, 100, 0, 40, None )
        self.game = game
        self.menu.menus = [('option1', test_func), ('option2', test_func2), ('option3', test_func3)]
        # self.game.run()

    def test_menu_move(self):
        self.menu.move(1)
        self.assertEqual(self.menu.option, 1)

    def test_menu_enter(self):
        self.assertEqual(self.menu.enter(), 1)

    def test_game_load(self):
        self.game.load('init.json')
        self.assertEqual(self.game.player.health, 100)
        self.assertEqual(self.game.player.exp, 0)
        self.assertEqual(self.game.player.attack, 40)
        self.assertEqual(self.game.player.speed, 5)

    def test_combat_attack_and_escape(self):
        self.game.load('init.json')  # must load first
        self.combat.attack()    # Attack the enemy
        self.assertEqual(self.game.player.health, 90)
        self.assertEqual(self.game.player.exp, 0)
        self.assertEqual(self.game.player.attack, 40)
        self.assertEqual(self.combat.enemy.health, 60)
        self.combat.escape()    # Escape
        self.assertEqual(self.game.player.health, 90)
        self.assertEqual(self.game.player.exp, 0)

    def test_gain_exp(self):
        self.game.load('init.json')
        self.combat.attack()
        self.combat.attack()
        self.combat.attack()    # Enemy died after being attacked three times
        self.assertEqual(self.game.player.exp, 10)  # Then the player's exp should be 10

    def test_player_move(self):
        self.assertEqual(self.player.attack, 40)    # test initialize correctly
        keys = create_key_mock(pg.K_DOWN)       # mock the K_DOWN  is pressed
        if keys[pg.K_LEFT]:
            self.player.rect[0] -= self.player.speed
        elif keys[pg.K_RIGHT]:
            self.player.rect[0] += self.player.speed
        elif keys[pg.K_UP]:
            self.player.rect[1] -= self.player.speed
        elif keys[pg.K_DOWN]:
            self.player.rect[1] += self.player.speed
        self.assertEqual(self.player.rect[1], 125)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
