import sys, time, random, math, pygame

import world as world
from pygame.locals import*
from mylibrary import*
from self import self
from world import*

class Player():
    def _init_ (self,game,level, name)：
        self.world = world
        self.alive = True
        self.y = 0
        self.name = "Antonio Salieri"
        self.experience = 0
        self.level = level
        self.weapon =  level
        self.weapon_name = "Baton"
        self.armor = level
        self.armor_name = "fancy coat"
        self.roll()

    def roll(self):
        self.str = 6 + Die(6) + Die(6)
        self.dex = 6 + Die(6) + Die(6)
        self.con = 6 + Die(6) + Die(6)
        self.int = 6 + Die(6) + Die(6)
        self.cha = 6 + Die(6) + Die(6)
        self.max_health = 10 + Die(self.con)
        self.health = self.max_health
    def levelUp(self):
        self.str += Die(6)
        self.dex += Die(6)
        self.con += Die(6)
        self.int += Die(6)
        self.cha += Die(6)
        self.max_health += Die(6)
        self.health = self.max_health
    def draw(self,surface,char):
        self.world.draw_char(surface,self.x,self.y,char)
    def move(self,movex,movey):
        char = self.world.getCharAt(self.x+movex,self.y+movey)
        if char not in (self.world.roomChar, self.world.hallChar):
            return False
        else:
            self.x += movex
            self.y += movey
            return True
    def moveUp(self):return self.move(0,-1)
    def moveDown(self):return self.move(0, 1)
    def moveLelf(self):return self.move(-1, 0)
    def moveRight(self):return self.move(1, 0)


    def addHealth(self,amount):
        self.health += amount
        if  self.health < 0:
            self.health = 0

    def addExperience(self,xp):
        cap = math.pow(10,self.level)
        self.experience += xp
        if self.experience > cap:
            self.levelUp()
    def getAttack(self):
        attack = self.str + Die(20)
        return attack
    def getDefence(self):
        defence =  self.dex + self.armor
        return defence
    def getDamage(self,defence):
        damage = Die(8) + self.str + self.weapon - defence
        return damage

    class Monster(Player):
        def _init_(self,world,level name):
        Player._init_(self,world,level,name)
        self.str = 1 + Die(6) + Die(6)
        self.dex = 1 + Die(6) + Die(6)
