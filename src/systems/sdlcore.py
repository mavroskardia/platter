import atexit
from sdl2 import *

from . import system
from ..config import config


class SdlInitSystem(system.System):

    def init(self, signaler):
        atexit.register(SDL_Quit)

        err = SDL_Init(SDL_INIT_EVERYTHING)

        if err != 0:
            raise Exception(SDL_GetError())

    def process(self, *args, signaler=None, entities=None, elapsed=0, **kargs):
        SDL_Delay(15)


class SdlWindowSystem(system.System):

    def init(self, signaler):
        err = SDL_VideoInit(None)

        if err != 0:
            raise Exception(SDL_GetError())

        self.window = SDL_CreateWindow(config.title.encode(),
                                       SDL_WINDOWPOS_CENTERED,
                                       SDL_WINDOWPOS_CENTERED,
                                       config.resolution[0],
                                       config.resolution[1],
                                       SDL_WINDOW_SHOWN)

        self.renderer = SDL_CreateRenderer(self.window, -1,
                                           SDL_RENDERER_ACCELERATED)

        self.register_events(signaler)
        self.clear()

    def register_events(self, signaler):
        pass

    def clear(self):
        SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
        SDL_RenderClear(self.renderer)

    def process(self, *args, signaler=None, entities=None, elapsed=0, **kargs):
        SDL_RenderPresent(self.renderer)
        self.clear()

    def register_events(self, signaler):
        signaler.register('draw:rect', self.draw_rect)
        signaler.register('draw:filledrect', self.draw_filled_rect)
        signaler.register('draw:texture', self.draw_texture)
        signaler.register(('_internal:'
                           'convert_surface_to_texture'),
                          self.convert_surface_to_texture)

    def draw_texture(self, position, size, texture, *args, **kwargs):
        SDL_RenderCopy(self.renderer, texture, None,
                       SDL_Rect(position.x, position.y, size.w, size.h))

    def draw_rect(self, position, size, *args, **kwargs):
        SDL_SetRenderDrawColor(self.renderer, 255, 255, 255, 255)
        SDL_RenderDrawRect(
            self.renderer,
            SDL_Rect(int(position.x), int(position.y),
                     int(size.w), int(size.h)))

    def draw_filled_rect(self, position, size, *args, **kwargs):
        SDL_SetRenderDrawColor(self.renderer, 255, 255, 255, 255)
        SDL_RenderFillRect(
            self.renderer,
            SDL_Rect(int(position.x), int(position.y),
                     int(size.w), int(size.h)))

    def convert_surface_to_texture(self, surface, callback):
        callback(SDL_CreateTextureFromSurface(self.renderer, surface))
