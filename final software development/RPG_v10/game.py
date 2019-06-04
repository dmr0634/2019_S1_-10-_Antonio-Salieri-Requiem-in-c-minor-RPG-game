import random

import pygame as pg

from entity import Game, Role, Enemy, GameMap, Pick, Sword, Shield, Npc, Skill
from scene import SceneM, Combat, Gameover, Dialog, YouWin, DialogGetDueEssay, DialogGetFinal
from utils import Vector2, openres, lazy

from other_games import snake
from other_games.tankwar.src.main import main as tankwar_main

Game._instance = None
game = Game()


class Final(Skill):
    name = 'Final'

    image = pg.transform.scale(
        openres(f'imgs/items/final.jpg'),
        (200, 200)
    )

    def __call__(self, sponsor, target):
        harm = target.health - target.health * 0.1
        target.health *= 0.1
        return harm


class DueEssay(Skill):
    name = 'Due Essay'

    image = pg.transform.scale(
        openres(f'imgs/items/due.jpg'),
        (200, 200)
    )

    def __call__(self, sponsor, target):
        target.health -= 40
        return min(40, target.health)


class WeaponTrigger:
    image = openres(f'imgs/npc.png').convert_alpha()

    def __init__(self):
        self.acc = 0

        self.triggers = {
            (7, 8): Npc(['Village was attacked by monsters!!']),
            (11, 18): self.final,
            (18, 12): self.due
        }

    def __call__(self, pos):
        self.acc += 1
        if self.acc == 3:
            game.map.triggers.update({
                (2, 3):
                    Pick(Sword('iron sword', 30, 5)),
                (1, 16):
                    Pick(Shield('wooden shield', 0, 20))
            })
        self.triggers[pos](pos)

    def final(self, pos):
        result = snake.main()
        if result:
            Pick(Final())(pos)
            Game().role.base_attack += 4
            Game().role.base_defense += 4
            SceneM().call(DialogGetFinal, ['Get skill Final'])
        else:
            SceneM().call(Dialog, ['You lose the game'])

    def due(self, pos):
        Game().map.triggers.pop(pos, None)
        result = tankwar_main()
        if result:
            Pick(DueEssay())(pos)
            Game().role.base_attack += 4
            Game().role.base_defense += 4
            SceneM().call(DialogGetDueEssay, ['Get skill Due Essay'])
        else:
            SceneM().call(Dialog, ['You lose the game'])


class EnemyTrigger:
    image = openres(f'imgs/npc.png').convert_alpha()

    def __init__(self, enemy, poses=()):
        self.enemy = enemy
        self.poses = poses

    def __call__(self, pos):
        game.map.triggers.pop(pos, None)
        for pos in self.poses:
            game.map.triggers.pop(pos, None)

        if len(game.role.equips) < 2:
            SceneM().call(Gameover)

        def onback():
            SceneM().call(YouWin)

        SceneM().call(Combat, self.enemy, onback=onback)


def update(elapse):
    if random.random() < 0.00001 * Game.mode.rate:
        enemy = Enemy('ghost', 30, 10, 10)
        SceneM().call(Combat, enemy)


game.update = update
game.map = GameMap(0)
game.role = Role(name='4', mpos=Vector2(11), health=100)

weapon_trigger = WeaponTrigger()
boss_trigger = EnemyTrigger(Enemy('boss', 100, 30, 20), ((34, 4), (35, 4)))

game.map.triggers = {
    (7, 8): weapon_trigger,
    (11, 18): weapon_trigger,
    (18, 12): weapon_trigger,
    (34, 4): boss_trigger,
    (35, 4): boss_trigger
}

game.maps = [game.map]
