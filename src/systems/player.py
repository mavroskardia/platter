from sdl2 import *

from . import system
from ..config import config
from ..math.vector import Vec
from ..components.player import PlayerControl
from ..components.physical import Body


class PlayerInputSystem(system.System):

    componenttypes = Body, PlayerControl

    acceleration = 50.0
    jump_force = Vec(0, -50.0)

    def init(self, signaler):
        signaler.register('keydown:Space', self.jump)
        self.initiate_jump = False

    def jump(self):
        self.initiate_jump = True

    def process(self, *args, signaler, components, elapsed, **kargs):
        kp = SDL_GetKeyboardState(None)

        for body, pc in components:
            if kp[SDL_SCANCODE_LEFT]:
                body.acc.x = -self.acceleration
            elif kp[SDL_SCANCODE_RIGHT]:
                body.acc.x = self.acceleration
            else:
                body.acc.x = 0

            if self.initiate_jump:
                self.initiate_jump = False
                body.acc += self.jump_force
