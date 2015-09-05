from sdl2 import *

from . import system
from ..components.player import PlayerControl
from ..components.physical import Acceleration


class PlayerSystem(system.System):

    componenttypes = Acceleration, PlayerControl

    acceleration = 10.0

    def process(self, *args, signaler=None, entities=None, elapsed=0, **kargs):
        kp = SDL_GetKeyboardState(None)

        self.y_acc = -self.acceleration if kp[SDL_SCANCODE_UP] else 0
        self.y_acc = self.acceleration if kp[SDL_SCANCODE_DOWN] else 0
        self.x_acc = -self.acceleration if kp[SDL_SCANCODE_LEFT] else 0
        self.x_acc = self.acceleration if kp[SDL_SCANCODE_RIGHT] else 0

        for e in entities:
            acc, pc = e.components
            acc.x = self.x_acc
            acc.y = self.y_acc
