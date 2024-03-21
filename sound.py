from pyglet.media import load, StaticSource

import os

sounds = {}

for filename in os.listdir('sounds/'):
    sound = StaticSource(load('sounds/' + filename))
    sound.play().pause() # force sound to load unlazily
    sounds.update({filename: sound})

def play_sound(name):
    sounds[name].play()