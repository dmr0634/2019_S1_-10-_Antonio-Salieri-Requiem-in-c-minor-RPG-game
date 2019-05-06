import unittest
RESOLUTION = 800, 600

import pygame as pg

pg.init()
screen = pg.display.set_mode(RESOLUTION)
pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])
from scene import MenuBase, Scene, Combat
from entity import game


def test_func():
    return 1


def test_func2():
    return 2


def test_func3():
    return 3


class TestGame(unittest.TestCase):

    def setUp(self):
        self.menu = MenuBase(Scene)
        self.combat = Combat(Scene)
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


if __name__ == '__main__':
    unittest.main(warnings='ignore')
