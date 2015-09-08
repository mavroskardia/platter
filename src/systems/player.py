from sdl2 import *

from . import system
from ..components.player import PlayerControl
from ..components.physical import Body, Jumping


class PlayerInputSystem(system.System):

    componenttypes = Body, PlayerControl

    acceleration = 50.0
    jump_force = -100.0

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
                signaler.trigger('add_component', Jumping(pc.entity))
