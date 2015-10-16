from sdl2 import *

from .system import System
from .. import config
from .. import signaler
from ..math.vector import Vec
from ..components.player import PlayerControl, PlayerData
from ..components.physical import Body


class PlayerDataSystem(System):

    componenttypes = PlayerData,

    def process(self, *args, components, elapsed, **kwargs):

        for pd, in components:
            signaler.instance.trigger(
                'draw:text', str(pd.score), SDL_Rect(0, 0, 0, 0))

            signaler.instance.trigger(
                'draw:text', str(pd.lives),
                SDL_Rect(config.resolution[0]-100, 0, 0, 0))


class PlayerInputSystem(System):

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

            signaler.instance.trigger('player:update', body)
