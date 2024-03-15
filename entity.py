from turtle import Turtle
from math import sin, cos

from constants import Constants

class Entity:
    def __init__(self, x, y, radius, speed, angle):
        self.speed = speed
        self.turtle = Turtle()
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.setpos(x, y)
        self.turtle.setheading(angle)
        self.set_radius(radius)

    def kill(self, entities):
        if self in entities:
            entities.remove(self)
        self.turtle.penup()
        self.turtle.hideturtle()

    def x(self):
        return self.turtle.xcor()

    def y(self):
        return self.turtle.ycor()

    def angle(self):
        return self.turtle.heading()

    def move(self):
        self.turtle.forward(self.speed)

    def rotate(self, angle):
        self.turtle.right(angle)

    def get_radius(self):
        return self.turtle.shapesize()[0] * Constants.MAGIC_NUMBER.value

    def set_radius(self, radius):
        self.turtle.shapesize(radius / Constants.MAGIC_NUMBER.value)

    def is_in_radius(self, x, y):
        return (self.x() - x)**2 + (self.y() - y)**2 <= self.get_radius()**2

    def wrap(self):
        if self.x() > Constants.BOUND.value:
            self.turtle.setx(-Constants.BOUND.value)
        elif self.x() < -Constants.BOUND.value:
            self.turtle.setx(Constants.BOUND.value)
        if self.y() > Constants.BOUND.value:
            self.turtle.sety(-Constants.BOUND.value)
        elif self.y() < -Constants.BOUND.value:
            self.turtle.sety(Constants.BOUND.value)

    def update(self, entities, scorekeeper):
        raise NotImplementedError

