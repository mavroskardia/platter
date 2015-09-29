import sys
from sdl2 import *

from .system import System


class InputSystem(System):

    def process(self, *args, signaler=None, entities=None, elapsed=0, **kargs):
        evt = SDL_Event()

        while SDL_PollEvent(evt):

            if evt.type == SDL_QUIT:
                signaler.trigger('quit')

            elif evt.type == SDL_KEYDOWN:
                s = evt.key.keysym.sym
                msg = 'keydown:{}'.format(SDL_GetKeyName(s).decode())
                signaler.trigger(msg)

            elif evt.type == SDL_KEYUP:
                s = evt.key.keysym.sym
                msg = 'keyup:{}'.format(SDL_GetKeyName(s).decode())
                signaler.trigger(msg)
