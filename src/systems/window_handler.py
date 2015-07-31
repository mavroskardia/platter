from sdl2 import *

from . import system
from ..config import config


class WindowHandler(system.System):

    def init(self, signaler):
        err = SDL_VideoInit(None)

        if err != 0:
            return False, SDL_GetError()

        self.window = SDL_CreateWindow(config.title.encode(),
                                       SDL_WINDOWPOS_CENTERED,
                                       SDL_WINDOWPOS_CENTERED,
                                       config.resolution[0],
                                       config.resolution[1],
                                       SDL_WINDOW_SHOWN)

        self.renderer = SDL_CreateRenderer(self.window, -1,
                                           SDL_RENDERER_ACCELERATED)

        return True, 'Initialized WindowHandler successfully'

    def update(self, signaler, componentdb):
        SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
        SDL_RenderClear(self.renderer)
        SDL_RenderPresent(self.renderer)
