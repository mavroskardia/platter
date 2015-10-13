from sdl2 import *

from . import system
from .. import config
from .. import signaler
from ..math.vector import Vec
from ..components.player import PlayerControl
from ..components.physical import Body


class PlayerInputSystem(system.System):

    componenttypes = Body, PlayerControl

    acceleration = 5.0
    jump_force = Vec(0, -200.0)

    def init(self):
        signaler.instance.register('keydown:Space', self.jump)
        self.initiate_jump = False

    def jump(self):
        self.initiate_jump = True

    def process(self, *args, components, elapsed, **kargs):
        kp = SDL_GetKeyboardState(None)

        for body, pc in components:
            if kp[SDL_SCANCODE_LEFT]:
                body.vel.x += -self.acceleration
            elif kp[SDL_SCANCODE_RIGHT]:
                body.vel.x += self.acceleration

            if self.initiate_jump:
                self.initiate_jump = False
                if not body.jumping:
                    body.jumping = True
                    body.vel += self.jump_force

            signaler.instance.trigger('player_update', body)
