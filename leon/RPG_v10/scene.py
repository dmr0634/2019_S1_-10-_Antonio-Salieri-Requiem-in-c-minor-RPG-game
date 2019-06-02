import os
import random
import pickle
from datetime import datetime

import pygame as pg

from entity import Game, Enemy, BasicSkill
from utils import openres, openrel, singleton, Vector2
from const import RESOLUTION, MU, FPS, UEvent, MODE, DIR, REST_INTERVAL

from other_games import snake


class Scene:
    def __init__(self, prev):
        self.prev = prev
        self.onback = None
        print('current scene: {}'.format(self.__class__))

    # 该方法每一帧运行一次
    def run(self, elapse):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.exit()
            elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                SceneM().back()
            else:
                # 事件处理
                self.handle_event(e)

        # 每一帧都要对场景进行更新
        self.update(elapse)

    def handle_event(self, event):
        pass

    def update(self, elapse):
        pass

    def render(self, screen):
        pass

    def exit(self):
        pg.quit()
        exit()


@singleton
class SceneM:
    'Scene Manager'

    class SceneSwitch(Exception):
        pass

    def __init__(self):
        self.scene = Start()
        self.timer = pg.time.Clock()
        self.screen = pg.display.get_surface()
        self.onback = None

    # 执行当前Scene的run方法然后刷新屏幕,并且保持60帧/秒的刷新速度
    def run(self):
        while True:
            elapse = self.timer.tick(FPS)

            try:
                self.scene.run(elapse)
            except self.SceneSwitch:
                pass

            self.scene.render(self.screen)
            pg.display.flip()

    # 切换Scene并且抛出一个SceneSwitch异常
    def switch(self, scene):
        self.scene = scene
        raise self.SceneSwitch()

    # 实例化一个Scene, 并且切换到这个Scene
    def call(self, scene_cls, *args, onback=None, **kw):
        scene = scene_cls(self.scene, *args, **kw)
        scene.onback = onback
        self.switch(scene)

    # 切换到上一个Scene
    def back(self, *args, **kw):
        if self.scene.onback:
            self.scene.onback(*args, **kw)
        self.switch(self.scene.prev or Start())


class Main(Scene):
    'Main interface'

    def __init__(self, prev=None):
        # 将主场景的prev属性初始化为Menu (在游戏中按Esc会弹出菜单)
        super().__init__(Menu(self))
        self.time = 0

    def handle_event(self, e):
        # 鼠标控制
        if e.type == pg.MOUSEBUTTONDOWN:
            dest = Vector2(e.pos) - Game().map.pos
            Game().role.goto(dest // MU)

        # 检查当前位置是否触发了事件
        elif e.type == UEvent.TRIGGER:
            trigger = Game().map.triggers.get(e.mpos)
            if trigger is not None:
                trigger(e.mpos)

        # 按空格键显示人物属性
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_SPACE:
                SceneM().call(RoleView)

    def update(self, elapse):
        self.time += elapse
        if self.time % REST_INTERVAL < elapse:
            m = self.time // 60000
            s = f"You've been playing for {m} minutes. Take a rest"
            SceneM().call(Dialog, [s])

        game = Game()
        game.update(elapse)

        # 控制人物移动，生成移动到的位置的事件
        game.role.logic()

        # 处理键盘输入，控制人物移动
        # 如果当前人物不在移动状态
        if not game.role.dest:
            # 通过键盘输入获取移动方向
            dir = DIR.from_keys(pg.key.get_pressed())
            # 如果方向键按下
            if dir is not None:
                # 获取下一个移动位置的坐标
                mdest = game.role.mpos + dir.unitvec
                mdest = int(mdest.x), int(mdest.y)
                # 如果下一个位置是可到达的位置，则将下一个位置的坐标加入移动路径
                if game.map.valid(mdest):
                    game.role.mpath = [mdest]

    def render(self, screen):
        gmap = Game().map
        role = Game().role

        # map bottom
        msurf = gmap.surf.copy()

        # 将所有触发器绘制出来(武器和盾牌)
        for pos, entity in gmap.triggers.items():
            msurf.blit(entity.image, Vector2(pos) * MU)

        # 绘制角色
        msurf.blit(role.image, role.pos)

        # 绘制房子顶部(遮挡角色)
        msurf.blit(gmap.surf_top, (0, 0))

        screen.blit(msurf, gmap.pos)


class Combat(Scene):
    frames = [(0, 0), (-10, 0), (10, 0)]

    def __init__(self, prev, enemy):
        super().__init__(prev)
        self.option = 0
        self.enemy = enemy
        self.enemy_total_health = enemy.health
        self.role = Game().role
        self.frame = 0
        self.battling = 0

    def run(self, elapse):
        for e in pg.event.get():
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    self.battle()
                elif e.key == pg.K_SPACE:
                    SceneM().call(RoleView)
                elif e.key == pg.K_DOWN:
                    self.option += 1
                elif e.key == pg.K_UP:
                    self.option -= 1
                self.option %= len(self.role.skills)

        if self.battling:
            self.frame = (self.frame + 1) % len(self.frames)
            self.battling -= 1

    def render(self, screen):
        screen.fill((255, 255, 255))

        frame = self.frames[self.frame]
        screen.blit(self.enemy.image, Vector2(130, 70) + frame)

        # 敌人血条
        hp_bar = pg.Surface((300, 20))
        hp_bar.fill((0, 0, 0))
        hp_bar.fill((255, 255, 255), (5, 5, 290, 10))
        hp_bar_length = int((self.enemy.health / self.enemy_total_health) * 290)
        hp_bar.fill((255, 0, 0), (5, 5, hp_bar_length, 10))

        # 绘制敌人血条
        screen.blit(hp_bar, (20, 20))

        for i, skill in enumerate(self.role.skills):
            color = (0, 0, 0) if i == self.option else (128, 128, 128)
            s = pg.font.Font(None, 42).render(str(skill), True, color)
            screen.blit(s, (460, 200 + i * 50))

    def battle(self):
        self.battling = 6

        skill = self.role.skills[self.option]
        harm = skill(self.role, self.enemy)
        text1 = 'You damaged the enemy {} hp with {}!'.format(harm, skill.name)
        if self.enemy.health <= 0:
            SceneM().back()

        skill = random.choice(self.enemy.skills)
        harm = skill(self.enemy, self.role)
        text2 = 'The enemy damaged you {} hp with {}!'.format(harm, skill.name)
        if self.role.health <= 0:
            SceneM().call(Gameover)

        SceneM().call(Dialog, [text2, text1])


class Help(Scene):
    'Tutorio interface'

    def run(self, elapse):
        if pg.event.get(pg.KEYDOWN):
            SceneM().back()

    def render(self, screen):
        help = openres('imgs/help.png')
        screen.blit(help, (0, 0))


class Gameover(Scene):
    def __init__(self, prev=None):
        return super().__init__(None)

    def render(self, screen):
        screen.fill((0, 0, 0))
        color = 200, 200, 200
        s = pg.font.Font(None, 42).render('Gameover', True, color)
        screen.blit(s, (240, 200))


class YouWin(Scene):
    def __init__(self, prev=None):
        return super().__init__(None)

    def render(self, screen):
        screen.fill((0, 0, 0))
        color = 200, 200, 200
        s = pg.font.Font(None, 42).render('You Win', True, color)
        screen.blit(s, (240, 200))


class MenuBase(Scene):
    'Main interface base flame'
    menus = []
    option = 0

    def handle_event(self, e):
        if self.menus and e.type == pg.KEYDOWN:
            if e.key == pg.K_DOWN:
                self.option += 1
            elif e.key == pg.K_UP:
                self.option -= 1
            else:
                self.menus[self.option][1]()
            self.option %= len(self.menus)

    def render(self, screen):
        screen.fill((0, 0, 0))
        for i, (menu, _) in enumerate(self.menus):
            color = (255, 255, 255) if i == self.option else (128, 128, 128)
            menu = pg.font.Font(None, 42).render(menu, True, color)
            screen.blit(menu, (54, 54 * i + 54))

    def update(self, elapse):
        pass


class SettingMenu(MenuBase):
    def __init__(self, prev):
        super().__init__(prev)
        self.update(0)

    def update(self, elapse):
        volume = int(pg.mixer.music.get_volume() * 10)
        self.menus = [(f'Volume:    {volume}', self.volume),
                      (f'Mode:      {str(Game.mode)}', self.mode)]

    def volume(self):
        keys = pg.key.get_pressed()
        volume = pg.mixer.music.get_volume()
        if keys[pg.K_LEFT]:
            volume -= 0.1
        elif keys[pg.K_RIGHT]:
            volume += 0.1
        pg.mixer.music.set_volume(volume)

    def mode(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            Game.mode -= 1
        elif keys[pg.K_RIGHT]:
            Game.mode += 1
        Game.mode = MODE.new(Game.mode)


class Menu(MenuBase):
    'Game menu'

    def __init__(self, prev):
        super().__init__(prev)
        self.menus = [('Continue', self.back_game),
                      ('Save Game', self.save_game), ('Setting', self.setting),
                      ('Start Menu', self.start_menu), ('Exit', self.exit)]

    def back_game(self):
        SceneM().back()

    def start_menu(self):
        SceneM().switch(Start())

    def save_game(self):
        dt = str(datetime.now()).replace(':', '-')
        fp = openrel(f'saves/{dt}.pkl', 'wb')
        pickle.dump(Game(), fp)

    def setting(self):
        SceneM().call(SettingMenu)


class Start(MenuBase):
    'Start interface'

    def __init__(self, prev=None):
        super().__init__(prev)
        self.menus = [('New Game', self.new_game),
                      ('Load Game', self.load_game), ('Setting', self.setting),
                      ('Exit', self.exit)]

    def new_game(self):
        import game
        import importlib
        importlib.reload(game)

        SceneM().switch(Help(Main()))

    def load_game(self):
        SceneM().call(Load)

    def setting(self):
        SceneM().call(SettingMenu)


class Load(MenuBase):
    'Loading file interface'

    def __init__(self, prev):
        super().__init__(prev)

        def load(fn):
            def func():
                Game._instance = openres(fn, 'rb')
                SceneM().switch(Main())

            return func

        saves = sorted(os.listdir('saves'), reverse=True)
        self.menus = [(fn, load(f'saves/{fn}')) for fn in saves]


class Dialog(Scene):
    surf = openres('imgs/dialog.png').convert_alpha()

    def __init__(self, prev, dialog):
        super().__init__(prev)
        self.dialog = dialog or ['...']

    def render(self, screen):
        self.prev.render(screen)

        surf = self.surf.copy()

        black = (255, 255, 255)
        s = pg.font.Font(None, 32).render(self.dialog[-1], True, black)
        surf.blit(s, (10, 10))

        screen.blit(surf, (0, 400))

    def handle_event(self, e):
        if e.type == pg.KEYDOWN or e.type == pg.MOUSEBUTTONDOWN:
            self.dialog.pop()
            if not self.dialog:
                SceneM().back()


class DialogGetDueEssay(Dialog):
    def render(self, screen):
        super().render(screen)

        from game import DueEssay
        image = DueEssay.image
        screen.blit(image, (220, 140))

        black = (255, 255, 255)
        s1 = pg.font.Font(None, 32).render('Base Attack +4', True, black)
        s2 = pg.font.Font(None, 32).render('Base Defense +4', True, black)
        screen.blit(s1, (220, 350))
        screen.blit(s2, (220, 370))


class DialogGetFinal(Dialog):
    def render(self, screen):
        super().render(screen)

        from game import Final
        image = Final.image
        screen.blit(image, (220, 140))

        black = (255, 255, 255)
        s1 = pg.font.Font(None, 32).render('Base Attack +4', True, black)
        s2 = pg.font.Font(None, 32).render('Base Defense +4', True, black)
        screen.blit(s1, (220, 350))
        screen.blit(s2, (220, 370))


class RoleView(Scene):
    surf = openres('imgs/roleview.png').convert_alpha()

    @property
    def image(self):
        role = Game().role

        surf = self.surf.copy()

        title = pg.font.Font(None, 28)
        text = pg.font.Font(None, 24)
        color = 200, 200, 200

        x, y = 32, 32

        health = title.render(f'{role.health}/{role.health_full}', True, color)
        surf.blit(role.image, (x, y))
        surf.blit(health, (x + 48, y + 12))
        y += 48

        for i, (cls, equip) in enumerate(role.equips.items()):
            surf.blit(equip.image, (x + i * 32, y))
        y += 48

        skill = title.render('Skills:', True, color)
        surf.blit(skill, (x, y))
        y += 32
        x += 16
        for i, skill in enumerate(role.skills):
            if isinstance(skill, BasicSkill):
                continue
            s = text.render(str(skill), True, color)
            surf.blit(s, (x, y))
            y += 32
        x -= 32

        return surf

    def handle_event(self, e):
        if e.type == pg.KEYDOWN:
            SceneM().back()

    def render(self, screen):
        self.prev.render(screen)
        screen.blit(self.image, (224, 48))


class Snake(Scene):
    def run(self, elapse):
        result = snake.main()
