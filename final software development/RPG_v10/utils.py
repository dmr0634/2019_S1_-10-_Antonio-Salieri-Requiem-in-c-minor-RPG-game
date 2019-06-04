import json
import pickle
from pathlib import Path

import pygame as pg
from pygame.math import Vector2


class lazy:
    def __init__(self, func: object) -> object:
        self.func = func

    def __get__(self, instance, cls):
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val


def openrel(fn, *args, **kw):
    path = Path(__file__).parent / fn
    return open(path, *args, **kw)


def openres(fn, *args, **kw):
    fp = openrel(fn, *args, **kw)

    if fn.endswith('.json'):
        return json.load(fp)

    if fn.endswith('.pkl'):
        return pickle.load(fp)

    if fn.endswith('.jpg') or fn.endswith('.png'):
        return pg.image.load(fp)


def singleton(cls):
    _instance = {}

    def func():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return func


class Singleton:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance


class Preservable:

    _ex = (pg.Surface, )

    def __getstate__(self):
        return {
            k: v
            for (k, v) in self.__dict__.items() if not isinstance(v, self._ex)
        }
