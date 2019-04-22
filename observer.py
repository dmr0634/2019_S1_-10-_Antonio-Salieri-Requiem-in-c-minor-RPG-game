"""
Module for all game observers.
"""
import pygame as pg
from . import constants as c
from . import setup

class Battle(object):
    """
    Observes events of battle and passes info to components.
    """
    def __init__(self, level):
        self.level = level
        self.player = level.player
        self.set_observer_for_enemies()
        self.event_dict = self.make_event_dict()

    def set_observer_for_enemies(self):
        for enemy in self.level.enemy_list:
            enemy.observers.append(self)

    def make_event_dict(self):
        """
        Make a dictionary of events the Observer can
        receive.
        """
        event_dict = {c.ENEMY_DEAD: self.enemy_dead,
                      c.ENEMY_DAMAGED: self.enemy_damaged,
                      c.PLAYER_DAMAGED: self.player_damaged}

        return event_dict

    def on_notify(self, event):
        """
        Notify Observer of event.
        """
        if event in self.event_dict:
            self.event_dict[event]()

    def player_damaged(self):
        self.level.enter_player_damaged_state()

    def enemy_damaged(self):
        """
        Make an attack animation over attacked enemy.
        """
        self.level.enter_enemy_damaged_state()

    def enemy_dead(self):
        """
        Eliminate all traces of enemy.
        """
        self.level.player.attacked_enemy = None


class SoundEffects(object):
    """
    Observer for sound effects.
    """
    def on_notify(self, event):
        """
        Observer is notified of SFX event.
        """
        if event in setup.SFX:
            setup.SFX[event].play()

class MusicChange(object):
    """
    Observer for special music events.
    """
    def __init__(self):
        self.event_dict = self.make_event_dict()

    def make_event_dict(self):
        """
        Make a dictionary with events keyed to new music.
        """
        new_dict = {c.BATTLE_WON: 'enchanted_festival'}
        return new_dict

    def on_notify(self, event):
        """
        Observer is notified of change in music.
        """
        if event in self.event_dict:
            new_music = self.event_dict[event]
            if new_music in setup.MUSIC:
                music_file = setup.MUSIC[new_music]
                pg.mixer.music.load(music_file)
                pg.mixer.music.play(-1)



















