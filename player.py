from math import sin, cos, radians
from random import randint
from time import sleep
from turtle import Turtle

from asteroid import Asteroid
from bullet import Bullet
from constants import Constants, Mutables
from entity import Entity

class Player(Entity):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, Constants.PLAYER_SIZE.value, 0, 0)
        self.vx = vx
        self.vy = vy
        self.direction = 0
        self.force = False
        self.toShoot = False
        self.isRespawning = False

    def x(self):
        return self.turtle.xcor()

    def y(self):
        return self.turtle.ycor()

    def angle(self):
        return self.turtle.heading()

    def nudge(self, angle):
        self.turtle.right(angle)

    def turn_left(self):
        self.direction = -1

    def turn_right(self):
        self.direction = 1

    def stop(self):
        self.direction = 0

    def thrust(self):
        self.force = True

    def stop_thrust(self):
        self.force = False

    def set_shoot(self, *args):
        self.toShoot = True

    def shoot(self, entities):
        entities.append(
            Bullet(
                self.x(),
                self.y(),
                Constants.BULLET_RAD.value,
                Constants.BULLET_SPEED.value,
                self.angle()
            )
        )

    def cap_speed(self):
        if self.vx > Constants.SPEED_CAP.value:
            self.vx = Constants.SPEED_CAP.value
        if self.vx < -Constants.SPEED_CAP.value:
            self.vx = -Constants.SPEED_CAP.value
        if self.vy > Constants.SPEED_CAP.value:
            self.vy = Constants.SPEED_CAP.value
        if self.vy < -Constants.SPEED_CAP.value:
            self.vy = -Constants.SPEED_CAP.value

    def respawn(self):
        b = int(Constants.BOUND.value / 4)

        self.turtle.setpos(
            randint(-b, b),
            randint(-b, b)
        )
        self.turtle.showturtle()
        self.vx = 0
        self.vy = 0
        self.isRespawning = False

    def update_dark_mode(self):
        if Mutables.dark_mode:
            self.turtle.fillcolor('white')
            self.turtle.pencolor('black')
        else:
            self.turtle.fillcolor('black')
            self.turtle.pencolor('white')

    def update(self, entities, scorekeeper):
        if not self.isRespawning:
            self.wrap()
        self.nudge(self.direction * Constants.NUDGE.value)
        if self.force:
            self.vx += Constants.THRUST.value * cos(radians(self.angle()))
            self.vy += Constants.THRUST.value * sin(radians(self.angle()))
        self.cap_speed()
        if self.toShoot:
            self.shoot(entities)
            self.toShoot = False
        self.turtle.setx(self.x() + self.vx)
        self.turtle.sety(self.y() + self.vy)
        for e in entities:
            if isinstance(e, Asteroid) and e.is_in_radius(self.x(), self.y()):
                e.split(entities, scorekeeper)
                if scorekeeper.lives > 0:
                    self.isRespawning = True
                    self.turtle.hideturtle()
                    self.turtle.setpos(1000, 1000)
                    self.turtle.getscreen().ontimer(
                        self.respawn,
                        2000
                    )
                else:
                    self.kill(entities)
                scorekeeper.lives -= 1
                return