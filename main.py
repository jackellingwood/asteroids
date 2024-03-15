from asteroid import Asteroid
from constants import Constants, Mutables
from player import Player
from scorekeeper import Scorekeeper

from colorsys import hsv_to_rgb
from math import sin, cos, radians
from random import randint
from turtle import Screen, Turtle, TurtleGraphicsError, Terminator
from time import sleep
from tkinter import TclError

def setup_screen():
    s = Screen()
    s.title('Pysteroids Alpha v0.2R')
    s.setup(Constants.BOUND.value * 2, Constants.BOUND.value * 2)
    s.tracer(0, 0)
    return s

def setup_entities():
    sk = Scorekeeper()
    player = Player(0, 0, 0, 0)
    entities = [*spawn_asteroids(), player]
    return entities, sk, player

def spawn_asteroids():
    asters = []
    for _ in range(5):
        if randint(0, 1) == 0:
            asters.append(
                Asteroid(
                    -Constants.BOUND.value,
                    randint(-300, 300),
                    Constants.ASTEROID_RAD.value,
                    randint(1, 20) * 0.1,
                    randint(0, 360)
                )
            )
        else:
            asters.append(
                Asteroid(
                    Constants.BOUND.value,
                    randint(-300, 300),
                    Constants.ASTEROID_RAD.value,
                    randint(1, 20) * 0.1,
                    randint(0, 360)
                )
            )
    for _ in range(5):
        if randint(0, 1) == 0:
            asters.append(
                Asteroid(
                    randint(-300, 300),
                    -Constants.BOUND.value,
                    Constants.ASTEROID_RAD.value,
                    randint(1, 20) * 0.1,
                    randint(0, 360)
                )
            )
        else:
            asters.append(
                Asteroid(
                    randint(-300, 300),
                    Constants.BOUND.value,
                    Constants.ASTEROID_RAD.value,
                    randint(1, 20) * 0.1,
                    randint(0, 360)
                )
            )
    return asters

def clear_keys(s):
    s.onkey(None, 'Left')
    s.onkey(None, 'Right')
    s.onkey(None, 'Up')
    s.onkey(None, 'Down')
    s.onkey(None, 'a')
    s.onkey(None, 'd')
    s.onkey(None, 'w')
    s.onkey(None, 's')
    s.onkey(None, 'space')
    s.onkey(None, 'Return')
    s.onclick(None)

def setup_controls(s, player):
    clear_keys(s)

    s.onkeypress(player.turn_left, 'Left')
    s.onkeyrelease(player.stop, 'Left')
    s.onkeypress(player.turn_right, 'Right')
    s.onkeyrelease(player.stop, 'Right')
    s.onkeypress(player.thrust, 'Up')
    s.onkeyrelease(player.stop_thrust, 'Up')
    s.onkey(player.set_shoot, 'space')

    s.onkeypress(player.turn_left, 'a')
    s.onkeyrelease(player.stop, 'a')
    s.onkeypress(player.turn_right, 'd')
    s.onkeyrelease(player.stop, 'd')
    s.onkeypress(player.thrust, 'w')
    s.onkeyrelease(player.stop_thrust, 'w')
    s.onclick(player.set_shoot)

    s.onkey(pause, 'Escape')

    s.onkey(restart, 'r')

    s.onkey(toggle_dark, 't')
    s.onkey(toggle_rainbow, 'g')

def setup_initials(s, scorekeeper):
    clear_keys(s)

    s.onkey(scorekeeper.decrement_pointer, 'Left')
    s.onkey(scorekeeper.increment_pointer, 'Right')
    s.onkey(scorekeeper.increment_initial, 'Up')
    s.onkey(scorekeeper.decrement_initial, 'Down')

    s.onkey(scorekeeper.decrement_pointer, 'a')
    s.onkey(scorekeeper.increment_pointer, 'd')
    s.onkey(scorekeeper.increment_initial, 'w')
    s.onkey(scorekeeper.decrement_initial, 's')

    s.onkey(scorekeeper.enter_initials, 'Return')

def pause():
    if Mutables.game_state != 'PAUSED':
        Mutables.last_state = Mutables.game_state
        Mutables.game_state = 'PAUSED'
    else:
        Mutables.game_state = Mutables.last_state

def restart():
    Mutables.game_state = 'RESTARTING'

def toggle_dark():
    Mutables.dark_mode = not Mutables.dark_mode

def toggle_rainbow():
    Mutables.rainbow_mode = not Mutables.rainbow_mode

def update_entities(entities, sk):
    for entity in entities:
        entity.update(entities, sk)

def update_color_mode(s, entities, scorekeeper):
    if Mutables.color_hue > 1:
        Mutables.color_hue = 0
    color = hsv_to_rgb(Mutables.color_hue, 1, 1)
    Mutables.color_hue += 0.01
    if Mutables.dark_mode:
        s.bgcolor('black')
    else:
        s.bgcolor('white')
    for entity in entities:
        entity.update_color_mode(color)
    scorekeeper.update_color_mode(color)

def game_loop(s, entities, sk):
    while Mutables.game_state != 'RESTARTING':
        if not Mutables.game_state == 'PAUSED':
            if sk.lives < 0:
                setup_initials(s, sk)
            if not any(isinstance(e, Asteroid) for e in entities):
                entities.extend(spawn_asteroids())
            s.listen()
            sleep(0.01)
            update_entities(entities, sk)
            update_color_mode(s, entities, sk)
            sk.update()
            s.update()
        else:
            s.listen()
            sleep(0.01)
            s.update()

def main():
    while True:
        Mutables.game_state = 'PLAYING'
        s = setup_screen()
        entities, sk, player = setup_entities()
        setup_controls(s, player)
        # sk.score = 10000
        # sk.lives = 0
        try:
            game_loop(s, entities, sk)
            s.clear()
        except (TclError, TurtleGraphicsError, Terminator, KeyboardInterrupt):
            return

if __name__ == "__main__":
    main()