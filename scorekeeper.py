from bisect import bisect
from pickle import dump, load
from turtle import Turtle

from constants import Constants, Mutables
from sound import play_sound

class Scorekeeper:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.nextTenK = 1
        self.turtle = Turtle()
        self.turtle.speed(0)
        self.turtle.hideturtle()
        self.turtle.setpos(-Constants.BOUND.value + 1, Constants.BOUND.value - 40)
        self.initials = 'AAA'
        self.initials_pointer = 0
        self.leaderboard = None

    def change_score(self, value):
        self.score += value

    def set_score(self, value):
        self.score = value

    def increment_initial(self):
        newChar = ''
        if self.initials[self.initials_pointer] == 'Z':
            newChar = ' '
        elif self.initials[self.initials_pointer] == ' ':
            newChar = 'A'
        else:
            newChar = chr(ord(self.initials[self.initials_pointer]) + 1)
        self.initials = (
                self.initials[:self.initials_pointer] +
                newChar +
                self.initials[self.initials_pointer + 1:]
        )
        play_sound('hit.wav')

    def decrement_initial(self):
        newChar = ''
        if self.initials[self.initials_pointer] == 'A':
            newChar = ' '
        elif self.initials[self.initials_pointer] == ' ':
            newChar = 'Z'
        else:
            newChar = chr(ord(self.initials[self.initials_pointer]) - 1)
        self.initials = (
            self.initials[:self.initials_pointer] +
            newChar +
            self.initials[self.initials_pointer + 1:]
        )
        play_sound('hit.wav')

    def increment_pointer(self):
        if self.initials_pointer < 2:
            self.initials_pointer += 1
        play_sound('hit.wav')

    def decrement_pointer(self):
        if self.initials_pointer > 0:
            self.initials_pointer -= 1
        play_sound('hit.wav')

    def enter_initials(self):
        if Mutables.game_state == 'ENTERING_INITIALS':
            self.edit_leaderboard()
            with open('leaderboard.pkl', 'wb') as f:
                dump(self.leaderboard, f)
            Mutables.game_state = 'GAME_OVER'
            play_sound('extralife.wav')

    def draw_leaderboard(self):
        self.turtle.setpos(-70, -25)
        self.turtle.write('RANK', False, 'center', ('Courier New', 10, 'normal'))

        self.turtle.setpos(0, -25)
        self.turtle.write('SCORE', False, 'center', ('Courier New', 10, 'normal'))

        self.turtle.setpos(70, -25)
        self.turtle.write('NAME', False, 'center', ('Courier New', 10, 'normal'))

        for index, entry in enumerate(self.leaderboard):
            name, score = entry
            rank = index + 1
            self.turtle.sety(-10 * rank - 30)
            self.turtle.setx(-70)
            self.turtle.write(rank, False, 'center', ('Courier New', 10, 'normal'))
            self.turtle.setx(0)
            self.turtle.write(score, False, 'center', ('Courier New', 10, 'normal'))
            self.turtle.setx(70)
            self.turtle.write(name, False, 'center', ('Courier New', 10, 'normal'))

    def edit_leaderboard(self):
        self.leaderboard = list(reversed(self.leaderboard))
        scores = [entry[1] for entry in self.leaderboard]
        idx = bisect(scores, self.score)
        self.leaderboard.insert(idx, (self.initials, self.score))
        self.leaderboard = list(reversed(self.leaderboard))
        self.leaderboard.pop()

    def update_color_mode(self):
        if Mutables.rainbow_mode:
            self.turtle.color(Mutables.color)
        elif Mutables.dark_mode:
            self.turtle.color('white')
        else:
            self.turtle.color('black')

    def update(self):
        self.turtle.setpos(-Constants.BOUND.value + 1, Constants.BOUND.value - 40)
        self.turtle.clear()
        self.turtle.penup()
        if self.score >= self.nextTenK * 10000:
            self.lives += 1
            self.nextTenK += 1
            play_sound('extralife.wav')

        self.turtle.write(self.score, False, font=('Courier New', 30, 'normal'))
        self.turtle.setpos(-Constants.BOUND.value + 8, Constants.BOUND.value - 40)
        self.turtle.setheading(90)
        if self.lives < 0:
            if self.leaderboard is None:
                try:  # if the leaderboard exists, read it in
                    with open('leaderboard.pkl', 'rb') as f:
                        self.leaderboard = load(f)
                except FileNotFoundError:  # if it doesn't, make a leaderboard
                    with open('leaderboard.pkl', 'wb') as f:
                        self.leaderboard = [
                            ('BOT', 1000000),
                            ('BOT', 500000),
                            ('BOT', 100000),
                            ('BOT', 75000),
                            ('BOT', 50000),
                            ('BOT', 30000),
                            ('BOT', 20000),
                            ('BOT', 10000)
                        ]
                        dump(self.leaderboard, f)
                if self.score > self.leaderboard[-1][1]:
                    Mutables.game_state = 'ENTERING_INITIALS'
                else:
                    Mutables.game_state = 'GAME_OVER'
        if Mutables.game_state == 'GAME_OVER':
            self.turtle.setpos(0, 0)
            self.turtle.write('GAME OVER', False, align='center', font=('Courier New', 30, 'normal'))
            self.draw_leaderboard()
        elif Mutables.game_state == 'ENTERING_INITIALS':
            self.turtle.setpos(0, 0)
            self.turtle.write('NEW HIGH SCORE', False, align='center', font=('Courier New', 30, 'normal'))
            self.turtle.sety(-19)
            self.turtle.write('ENTER INITIALS', False, align='center', font=('Courier New', 15, 'normal'))
            self.turtle.sety(-40)
            self.turtle.write(self.initials, False, align='center', font=('Courier New', 15, 'normal'))
            self.turtle.setx(((self.initials_pointer - 1) * 12) - 1)
            self.turtle.stamp()
        elif Mutables.game_state == 'PLAYING':
            for i in range(self.lives):
                self.turtle.stamp()
                self.turtle.setx(self.turtle.xcor() + 12)
