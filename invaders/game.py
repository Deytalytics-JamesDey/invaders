import sys
import random

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

from .entities import Invader, Fleet

class InvadersGame(Widget):
    score = 0
    wave = 1
    refresh = False
    move_time = 0.1

    def __init__(self):
        super(InvadersGame, self).__init__()

        self.size = (400, 400)
        self._entities = []

        self._add_entity(self.player_ship, skip_widget=True)
        self._init_fleet(self.move_time)

        self._music = SoundLoader.load('sounds/DST-DFear.mp3')
        self._music.play()


    def update(self, dt):
        self.fleet.update(dt)
        for e in self._entities[:]:
            status = e.update(dt)
            if not status or e.collision_detected:
                if e.collision_detected:
                    self.score += 1
                    self.ids['scorelabel'].text = "SCORE: " + str(self.score)
                self._remove_entity(e)
                if self.score % 50 == 0 and (len(self._entities)==1 or (len(self._entities) > 1 and self._entities[1]=="Bullet"))  and self.refresh == False:
                    refresh=True
                    self.wave += 1
                    self.ids['wavelabel'].text = "WAVE: " + str(self.wave)
                    self.move_time*=0.9
                    self.size = (400, 400)
                    self._init_fleet(self.move_time)
                    refresh=False

    def leftButton(self, *args):
        self.player_ship.move_direction = -1

    def rightButton(self, *args):
        self.player_ship.move_direction = 1


    def on_touch_down(self, touch):
        C = [a - b for a, b in zip(touch.pos, self.player_ship.pos)]
        if C[0] in range(50):
            bullets = [e for e in self._entities if e.name == 'Bullet']
            if len(bullets) < 2:
                bullet = self.player_ship.fire()
                self._add_entity(bullet)
        if touch.pos[0] < self.player_ship.x-50 and touch.pos[1]<200:
            Clock.schedule_interval(self.move_left, 0)

        if touch.pos[0] > self.player_ship.x+50 and touch.pos[1] < 200:
            Clock.schedule_interval(self.move_right, 0)

    def on_touch_up(self, touch):
        Clock.unschedule(self.move_left)
        Clock.unschedule(self.move_right)

    def move_left(self, dt):
        self.player_ship.x -= 10

    def move_right(self, dt):
        self.player_ship.x += 10

    def _init_fleet(self,move_time):
        self.fleet = Fleet(rows=5, cols=10, move_time=self.move_time)
        self.fleet.pos = ((self.width - self.fleet.width) / 2 + 50, 0)
        self.add_widget(self.fleet)

        self.fleet.create_fleet()
        for s in self.fleet.ships:
            self._add_entity(s)

    def _add_entity(self, entity, skip_widget=False):
        self._entities.append(entity)
        if not skip_widget:
            self.add_widget(entity)

    def _remove_entity(self, entity):
        self.remove_widget(entity)
        self._entities.remove(entity)
