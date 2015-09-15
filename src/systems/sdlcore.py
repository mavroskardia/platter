import atexit

from sdl2 import *
from sdl2.sdlttf import *

from . import system
from .. import config


class SdlInitSystem(system.System):

    def init(self, signaler):
        atexit.register(SDL_Quit)

        err = SDL_Init(SDL_INIT_EVERYTHING)

        if err != 0:
            raise Exception(SDL_GetError())

    def process(self, *args, signaler=None, entities=None, elapsed=0, **kargs):
        SDL_Delay(1)


class SdlWindowSystem(system.System):

    def init(self, signaler):
        err = SDL_VideoInit(None)

        if err != 0:
            raise Exception(SDL_GetError())

        err = TTF_Init()

        if err != 0:
            raise Exception(TTF_GetError())

        self.window = SDL_CreateWindow(config.title.encode(),
                                       SDL_WINDOWPOS_CENTERED,
                                       SDL_WINDOWPOS_CENTERED,
                                       config.resolution[0],
                                       config.resolution[1],
                                       SDL_WINDOW_SHOWN)

        self.renderer = SDL_CreateRenderer(self.window, -1,
                                           SDL_RENDERER_ACCELERATED)

        self.font = TTF_OpenFont(config.hud_font.encode(),
                                 config.hud_font_size)
        if not self.font:
            raise Exception(TTF_GetError())

        self.register_events(signaler)
        self.clear()

    def clear(self):
        SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
        SDL_RenderClear(self.renderer)

    def process(self, *args, signaler=None, entities=None, elapsed=0, **kargs):
        SDL_RenderPresent(self.renderer)
        self.clear()

    def register_events(self, signaler):
        signaler.register('get_renderer', self.get_renderer)
        signaler.register('draw:rect', self.draw_rect)
        signaler.register('draw:filledrect', self.draw_filled_rect)
        signaler.register('draw:texture', self.draw_texture)
        signaler.register('draw:text', self.draw_text)
        signaler.register('_internal:convert_surface_to_texture',
                          self.convert_surface_to_texture)

    def get_renderer(self, callback):
        callback(self.renderer)

    def draw_texture(self, texture, x, y, w, h, *args, **kwargs):
        SDL_RenderCopy(self.renderer, texture, None,
                       SDL_Rect(int(x), int(y), int(w), int(h)))

    def draw_rect(self, body, *args, **kwargs):
        SDL_SetRenderDrawColor(self.renderer, 255, 255, 255, 255)
        SDL_RenderDrawRect(self.renderer,
                           SDL_Rect(int(body.pos.x), int(body.pos.y),
                                    int(body.w), int(body.h)))

    def draw_filled_rect(self, body, *args, **kwargs):
        SDL_SetRenderDrawColor(self.renderer, 255, 255, 255, 255)
        SDL_RenderFillRect(self.renderer,
                           SDL_Rect(int(body.pos.x), int(body.pos.y),
                                    int(body.w), int(body.h)))

    def convert_surface_to_texture(self, surface, callback):
        callback(SDL_CreateTextureFromSurface(self.renderer, surface))

    def draw_text(self, body, text, *args, **kwargs):
        t = TTF_RenderUTF8_Blended(self.font, text.text.encode(),
                                   SDL_Color(255, 255, 255, 255))
        tex = SDL_CreateTextureFromSurface(self.renderer, t)
        body.w, body.h = t.contents.w, t.contents.h
        SDL_RenderCopy(self.renderer, tex, None,
                       SDL_Rect(int(body.pos.x), int(body.pos.y),
                                int(body.w), int(body.h)))
