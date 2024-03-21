from asteroid import Asteroid

from constants import Constants, Mutables
from entity import Entity
from sound import play_sound

class Bullet(Entity):
    def __init__(self, x, y, radius, speed, angle):
        super().__init__(x, y, radius, speed, angle)
        self.turtle.shape('circle')

    def anti_wrap(self, entities):
        if self.x() > Constants.BOUND.value:
            self.kill(entities)
        elif self.x() < -Constants.BOUND.value:
            self.kill(entities)
        if self.y() > Constants.BOUND.value:
            self.kill(entities)
        elif self.y() < -Constants.BOUND.value:
            self.kill(entities)

    def update_dark_mode(self):
        if Mutables.dark_mode:
            self.turtle.color('white')
        else:
            self.turtle.color('black')

    def update(self, entities, scorekeeper):
        self.anti_wrap(entities)
        self.move()
        for e in entities:
            if isinstance(e, Asteroid) and e.is_in_radius(self.x(), self.y()):
                e.split(entities, scorekeeper)
                self.kill(entities)
                play_sound('hit.wav')
                return
