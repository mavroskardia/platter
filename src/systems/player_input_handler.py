import sys
from sdl2 import *

from . import system
from ..components.player_controls import PlayerControls


class PlayerInputHandler(system.System):

    componenttypes = PlayerControls,

    def init(self, signaler):
        self.moving = {SDL_SCANCODE_UP: False, SDL_SCANCODE_DOWN: False,
                       SDL_SCANCODE_LEFT: False, SDL_SCANCODE_RIGHT: False}

    def process(self, signaler, components):
        kp = SDL_GetKeyboardState(None)

        for pc, in components:
            for k in self.moving.keys():
                kn = SDL_GetKeyName(SDL_GetKeyFromScancode(k)).decode()
                if self.moving[k] and not kp[k]:
                    self.moving[k] = False
                    signaler.trigger('player:{}'.format(kn), pc.entity,
                                     self.moving[k])
                elif not self.moving[k] and kp[k]:
                    self.moving[k] = True
                    signaler.trigger('player:{}'.format(kn), pc.entity,
                                     self.moving[k])
