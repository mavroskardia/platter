import atexit
from sdl2 import *

from . import system


class SdlCoreHandler(system.System):

    def init(self, signaler):
        atexit.register(SDL_Quit)

        err = SDL_Init(SDL_INIT_EVERYTHING)

        if err != 0:
            return False, SDL_GetError()

        return True, 'Initialized SDL successfully'

    def update(self, signaler, componentdb):
        SDL_Delay(15)
