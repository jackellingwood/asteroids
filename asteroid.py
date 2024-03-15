from constants import Constants, Mutables
from entity import Entity

from random import randint

class Asteroid(Entity):
    def __init__(self, x, y, radius, speed, angle):
        super().__init__(x, y, radius, speed, angle)
        self.turtle.shape('circle')
        self.turtle.fillcolor('white')

    def split(self, entities, scorekeeper):
        scorekeeper.change_score(int(Constants.SCORE_NUMERATOR.value / self.get_radius()))
        if self.get_radius() < Constants.ASTEROID_RAD.value / Constants.MAGIC_NUMBER.value * 4:
            self.kill(entities)
            return
        splitAngle = randint(0, 160)
        currAngle = -splitAngle/2
        for _ in range(Constants.SPLIT_AMOUNT.value):
            a = Asteroid(self.x(), self.y(), self.get_radius() / Constants.SPLIT_AMOUNT.value, randint(1, 20) * 0.1, self.angle())
            a.move()
            a.rotate(currAngle + randint(-5, 5))
            currAngle += splitAngle / (Constants.SPLIT_AMOUNT.value - 1)
            entities.append(a)
        self.kill(entities)

    def update_dark_mode(self):
        if Mutables.dark_mode:
            self.turtle.fillcolor('black')
            self.turtle.pencolor('white')
        else:
            self.turtle.fillcolor('white')
            self.turtle.pencolor('black')

    def update(self, entities, scorekeeper):
        self.wrap()
        self.move()