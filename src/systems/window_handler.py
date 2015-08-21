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

        self.register_events(signaler)

        self.clear()

        return True, 'Initialized WindowHandler successfully'

    def clear(self):
        SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
        SDL_RenderClear(self.renderer)

    def update(self, signaler, componentdb):
        SDL_RenderPresent(self.renderer)
        self.clear()

    def register_events(self, signaler):
        signaler.register('draw:rect', self.draw_rect)
        signaler.register('draw:texture', self.draw_texture)
        signaler.register(('_internal:'
                           'convert_surface_to_texture_and_add_to_tileset'),
                          self.convert_surface_to_texture_and_add_to_tileset)

    def draw_texture(self, position, size, texture, *args, **kwargs):
        SDL_RenderCopy(self.renderer, texture, None,
                       SDL_Rect(position.x, position.y, size.w, size.h))

    def draw_rect(self, position, size, *args, **kwargs):
        SDL_SetRenderDrawColor(self.renderer, 255, 255, 255, 255)
        SDL_RenderDrawRect(
            self.renderer,
            SDL_Rect(int(position.x), int(position.y), size.w, size.h))

    def convert_surface_to_texture_and_add_to_tileset(self, tileset, surface,
                                                      tilename):

        t = SDL_CreateTextureFromSurface(self.renderer, surface)
        tileset[tilename] = t
