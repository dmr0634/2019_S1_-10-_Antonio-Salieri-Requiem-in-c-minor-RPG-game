import json
from pathlib import Path

import pygame as pg


def relpath(fn):
    return Path(__file__).parent / fn


def openres(fn):
    path = relpath(fn)
    if fn.endswith('.json'):
        with open(path) as file:
            return json.load(file)
    elif fn.endswith('.jpg') or fn.endswith('.png'):
        return pg.image.load(fn)
