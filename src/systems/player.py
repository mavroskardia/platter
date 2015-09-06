from sdl2 import *

from . import system
from ..components.player import PlayerControl
from ..components.physical import Acceleration


class PlayerSystem(system.System):

    componenttypes = Acceleration, PlayerControl

    acceleration = 50.0
    jump_force = -100.0

    def init(self, signaler):
        self.acc_y = 0.0
        self.initiate_jump = False
        self.jumping = False
        signaler.register('keydown:Space', self.jump)

    def jump(self):
        self.initiate_jump = True

    def process(self, *args, s=None, components=None, elapsed=0, **kargs):
        kp = SDL_GetKeyboardState(None)

        for acc, pc in components:
            if kp[SDL_SCANCODE_LEFT]:
                acc.x = -self.acceleration
            elif kp[SDL_SCANCODE_RIGHT]:
                acc.x = self.acceleration
            else:
                acc.x = 0

            if self.initiate_jump:
                print('jumping')
                acc.y = self.jump_force
                self.initiate_jump = False
