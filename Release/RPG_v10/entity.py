import pygame as pg
import numpy as np
from pygame import Rect

from utils import openres, openrel, Vector2, Singleton, Preservable, lazy
from const import MU, RESOLUTION, UEvent, DIR, MODE
from astar import AStar


class Game:
    _instance = None
    mode = MODE.NORMAL

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def update(self, elapse):
        pass


class GameMap(Preservable):

    @lazy
    def surf(self):
        return openres(f'maps/{self.iid}/bottom.png').convert_alpha()

    @lazy
    def surf_top(self):
        return openres(f'maps/{self.iid}/top.png').convert_alpha()

    def __init__(self, iid, **kw):
        self.iid = iid
        self.triggers = {}
        fp = openrel(f'maps/{iid}/map', 'rb')
        self._map = np.load(fp, allow_pickle=True)
        self.__dict__.update(kw)

    @property
    def w(self):
        return self._map.shape[0]

    @property
    def h(self):
        return self._map.shape[1]

    def valid(self, mpos):
        x, y = mpos
        if x < 0 or y < 0:
            return False
        try:
            return not self[x][y]
        except:
            return False

    @property
    def pos(self):
        # Let character keep in the middle of screen
        pos = Game().role.pos - Vector2(RESOLUTION) / 2

        # 使窗口在地图内
        win = Rect(pos, RESOLUTION)
        win.clamp_ip(self.surf.get_rect())

        # 变换为窗口坐标系
        return -Vector2(win.topleft)

    def __getitem__(self, item):
        return self._map[item]


class CharWalk(Preservable):

    step = 4
    framec = 3

    @lazy
    def surf(self):
        return openres(f'imgs/role/{self.name}.png').convert_alpha()

    def __init__(self, name, mpos):
        super().__init__()
        self.name = name

        # 人物坐标(真实的地图像素坐标)
        self.pos = mpos * MU

        self.dir = DIR.DOWN
        self.frame = 1 * MU
        self.dest = None
        self.mpath = []

    @property
    def image(self):
        # 获取当前的人物图像
        # 第几列: 根据当前的帧次
        # 第几行: 根据移动方向 self.dir * MU
        sub = Rect(self.frame // MU * MU, self.dir * MU, MU, MU)
        return self.surf.subsurface(sub)

    # 获取当前人物坐标
    @property
    def mpos(self):
        return (self.dest or self.pos) // MU

    def logic(self):
        if self.dest is None:
            # 路径不为空
            if not self.mpath:
                return
            # 获取下一个移动目的地坐标
            mdest = self.mpath.pop()
            # 生成该坐标的事件
            event = pg.event.Event(UEvent.TRIGGER, mpos=mdest)
            # 将该事件添加到事件队列
            pg.event.post(event)

            # 将目的地位置转化为真实的像素坐标
            self.dest = Vector2(mdest) * MU
            # 获取移动方向
            self.dir = DIR.from_vec(self.dest - self.pos)

        # 将人物移动一个步长
        self.pos += Vector2(self.dir.unitvec) * self.step

        # 用来获取当前帧次的人物图像
        self.frame += self.framec * self.step
        self.frame %= self.framec * MU

        # 如果移动到目的地，则将目的地坐标置为空
        if self.pos == self.dest:
            self.dest = None

    def goto(self, mdest):
        src = [int(i) for i in self.mpos]
        dst = [int(i) for i in mdest]
        path = AStar(Game().map, src, dst).start() or []
        self.mpath = [(i.x, i.y) for i in reversed(path)]


class Skill(Singleton):
    name = None

    def __str__(self):
        return str(self.name or self.__class__.__name__)

    def __call__(self, sponsor, target):
        pass


class BasicSkill(Skill):
    pass


class Escape(BasicSkill):
    def __call__(self, sponsor, target):
        from scene import SceneM
        SceneM().back()


class Attack(BasicSkill):
    name = 'Attack'
    def __call__(self, sponsor, target):
        harm = max(0, sponsor.atk - target.dfs)
        target.health -= harm
        return harm


class Role(CharWalk):
    def __init__(self, name, mpos, health, health_full=None, **kw):
        super().__init__(name, mpos)
        self.items = []
        self.equips = {}
        # 当前生命值
        self.health = health
        # 最大生命值
        self.health_full = health_full or health
        # 拥有技能
        self.skills = [Attack(), Escape()]
        # 基础攻击
        self.base_attack = 0
        # 基础防御
        self.base_defense = 0

        self.__dict__.update(kw)

    def take(self, item):
        if isinstance(item, Equipment):
            cls = item.__class__
            origin = self.equips.pop(cls, None)
            if origin:
                self.items.append(origin)
            self.equips[cls] = item
        elif isinstance(item, Skill):
            self.skills.append(item)
        else:
            self.items.append(item)

    # 攻击力
    @property
    def atk(self):
        return sum(e.atk for e in self.equips.values()) + self.base_attack

    # 防御力
    @property
    def dfs(self):
        return sum(e.dfs for e in self.equips.values()) + self.base_defense


class Equipment(Preservable):

    @lazy
    def image(self):
        name = self.name.replace(' ', '-')
        return openres(f'imgs/items/{name}.png').convert_alpha()

    def __init__(self, name, atk, dfs):
        self.name = name
        self.atk = atk
        self.dfs = dfs


class Sword(Equipment):
    pass


class Shield(Equipment):
    pass


class Pick:
    @property
    def image(self):
        return self.item.image

    def __init__(self, item):
        self.item = item

    def __call__(self, pos):
        Game().map.triggers.pop(pos, None)
        Game().role.take(self.item)


class Npc:
    image = openres(f'imgs/npc.png').convert_alpha()

    def __init__(self, dialog):
        self.dialog = dialog

    def __call__(self, pos):
        from scene import SceneM, Dialog
        Game().map.triggers.pop(pos, None)
        SceneM().call(Dialog, self.dialog)


class Enemy:

    @lazy
    def image(self):
        return openres(f'imgs/enemy/{self.name}.png').convert_alpha()

    def __init__(self, name, health, atk, dfs, skills=()):
        self.name = name
        self.health = health * Game.mode.rate
        self.atk = atk * Game.mode.rate
        self.dfs = dfs * Game.mode.rate
        self.skills = [Attack()]
        self.skills.extend(skills)
