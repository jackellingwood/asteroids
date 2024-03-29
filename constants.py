from colorsys import hsv_to_rgb
from enum import Enum

class Constants(Enum):
    BOUND = 300
    SPLIT_AMOUNT = 2
    NUDGE = 3
    THRUST = 0.03
    MAGIC_NUMBER = 10
    ASTEROID_RAD = 50
    BULLET_SPEED = 7
    BULLET_RAD = 1
    PLAYER_SIZE = 12
    SCORE_NUMERATOR = 1250
    SPEED_CAP = 15

class Mutables:
    dark_mode = True
    rainbow_mode = False
    color_hue = 0
    color = hsv_to_rgb(color_hue, 1, 1)
    game_state = 'PLAYING'
    last_state = 'PLAYING'
    round = 0