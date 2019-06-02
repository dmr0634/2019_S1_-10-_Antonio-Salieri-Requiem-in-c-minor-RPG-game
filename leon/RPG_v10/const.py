from enum import IntEnum, unique

import pygame as pg
from pygame import USEREVENT

from utils import lazy

MU = 32     # map unit size
STEP = 4    # role speed

FPS = 60
RESOLUTION = 640, 480

REST_INTERVAL = 2 * 60 * 1000


class UEvent(IntEnum):
    TRIGGER = USEREVENT + 5


@unique
class DIR(IntEnum):
    DOWN = 0
    LEFT = 1
    RIGHT = 2
    UP = 3

    @lazy
    def unitvec(self):
        return [(0, 1), (-1, 0), (1, 0), (0, -1)][self]

    @classmethod
    def from_keys(cls, keys):
        if keys[pg.K_LEFT]:
            return cls.LEFT
        if keys[pg.K_RIGHT]:
            return cls.RIGHT
        if keys[pg.K_UP]:
            return cls.UP
        if keys[pg.K_DOWN]:
            return cls.DOWN

    @classmethod
    def from_vec(cls, vec):
        x, y = vec
        if x < 0:
            return cls.LEFT
        if x > 0:
            return cls.RIGHT
        if y < 0:
            return cls.UP
        if y > 0:
            return cls.DOWN


@unique
class MODE(IntEnum):
    EASY = 0
    NORMAL = 1
    HARD = 2
    EXTREME = 3
    HELL = 4
    _MAX = 5

    @property
    def rate(self):
        return [0.5, 1, 2, 4, 6][self]

    def __str__(self):
        return ['easy', 'normal', 'hard', 'extreme', 'hell'][self]

    @classmethod
    def new(cls, i):
        return cls(i % cls._MAX)
