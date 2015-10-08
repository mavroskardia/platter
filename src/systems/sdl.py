import atexit

from sdl2 import *
from sdl2.sdlttf import *

from .system import System
from .. import config
from .. import signaler


class SdlSystem(System):

    def init(self):
        atexit.register(SDL_Quit)

        err = SDL_Init(SDL_INIT_EVERYTHING)
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

        self.register_events()
        self.clear()

    def clear(self):
        SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
        SDL_RenderClear(self.renderer)

    def process(self, *args, entities=None, elapsed=0, **kargs):
        SDL_RenderPresent(self.renderer)
        self.clear()
        SDL_Delay(5)

    def register_events(self):
        s = signaler.instance
        s.register('get_renderer', self.get_renderer)
        s.register('draw:rect', self.draw_rect)
        s.register('draw:line', self.draw_line)
        s.register('draw:filledrect', self.draw_filled_rect)
        s.register('draw:texture', self.draw_texture)
        s.register('draw:text', self.draw_text)
        s.register('_internal:convert_surface_to_texture',
                   self.convert_surface_to_texture)

    def get_renderer(self, callback):
        callback(self.renderer)

    def draw_texture(self, texture, rect, *args, **kwargs):
        r = SDL_Rect(int(rect.x), int(rect.y), int(rect.w), int(rect.h))
        SDL_RenderCopy(self.renderer, texture, None, r)

    def draw_rect(self, rect, *args, **kwargs):
        r = SDL_Rect(int(rect.x), int(rect.y), int(rect.w), int(rect.h))
        SDL_SetRenderDrawColor(self.renderer, 255, 255, 255, 255)
        SDL_RenderDrawRect(self.renderer, r)

    def draw_line(self, x1, y1, x2, y2, *args, **kwargs):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        SDL_SetRenderDrawColor(self.renderer, 255, 255, 255, 255)
        SDL_RenderDrawLine(self.renderer, x1, y1, x2, y2)

    def draw_filled_rect(self, rect, *args, **kwargs):
        r = SDL_Rect(int(rect.x), int(rect.y), int(rect.w), int(rect.h))
        SDL_SetRenderDrawColor(self.renderer, 255, 255, 255, 255)
        SDL_RenderFillRect(self.renderer, r)

    def convert_surface_to_texture(self, surface, callback, *args):
        tex = SDL_CreateTextureFromSurface(self.renderer, surface)
        callback(tex, surface.contents.w, surface.contents.h, *args)

    def draw_text(self, text, rect, *args, **kwargs):
        c = SDL_Color(255, 255, 255, 255)
        t = TTF_RenderUTF8_Blended(self.font, text.encode(), c)
        r = SDL_Rect(int(rect.x), int(rect.y), t.contents.w, t.contents.h)
        tex = SDL_CreateTextureFromSurface(self.renderer, t)
        SDL_RenderCopy(self.renderer, tex, None, r)
