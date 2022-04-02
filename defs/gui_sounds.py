# PyQt5 Fancy-Stuff
from PyQt5 import QtMultimedia

# Defs
from defs.japa4551 import *
from defs import sounds_path


class PlaySound():
    def Success():
        QtMultimedia.QSound.play(sounds_path + "success_bell-6776.wav")

    def Failed():
        QtMultimedia.QSound.play(sounds_path + "mixkit-electric-buzz-glitch-2594.wav")


