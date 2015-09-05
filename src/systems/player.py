from sdl2 import *

from . import system
from ..components.player import PlayerControl
from ..components.physical import Acceleration


class PlayerSystem(system.System):

    componenttypes = Acceleration, PlayerControl

    acceleration = 100.0

    def process(s, *args, signaler=None, components=None, elapsed=0, **kargs):
        kp = SDL_GetKeyboardState(None)

        if kp[SDL_SCANCODE_UP]:
            s.y_acc = -s.acceleration
        elif kp[SDL_SCANCODE_DOWN]:
            s.y_acc = s.acceleration
        else:
            s.y_acc = 0

        if kp[SDL_SCANCODE_LEFT]:
            s.x_acc = -s.acceleration
        elif kp[SDL_SCANCODE_RIGHT]:
            s.x_acc = s.acceleration
        else:
            s.x_acc = 0

        for acc, pc in components:
            acc.x = s.x_acc
            acc.y = s.y_acc
