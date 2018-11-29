import atexit

from sdl2 import *
from sdl2.sdlttf import *

from .system import System
from .. import config
from .. import signaler
from ..math.vector import Vec


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

        SDL_SetRenderDrawBlendMode(self.renderer, SDL_BLENDMODE_BLEND)

        self.middle = Vec(config.resolution[0] / 2, config.resolution[1] / 2)
        self.offset = Vec(0, 0)
        self.register_events()

    def process(self, *args, entities=None, elapsed=0, **kargs):
        SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
        SDL_RenderClear(self.renderer)
        SDL_RenderPresent(self.renderer)
        SDL_Delay(5)

    def translate(self, x, y):
        return int(x + self.offset.x), int(y + self.offset.y)

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
        s.register('player:update', self.update_offset)

    def update_offset(self, body):
        return
        if body.pos.x > self.offset.x + self.middle.x:
            # player is right-of-center, correct offset so it's centered
            self.offset.x -= 1
        elif body.pos.x < self.offset.x + self.offset.x:
            # player is left-of-center, correct offset so it's centered
            self.offset.x += 1

        # make sure never fly off the left-side of the map
        self.offset.x = max(0, self.offset.x)
        # temporarily prevent flying off the right-side of the map
        self.offset.x = min(10000, self.offset.x)

        # constant value gives feeling of a auto-scrolling world
        # self.offset.x -= 1

    def get_renderer(self, callback):
        callback(self.renderer)

    def draw_texture(self, texture, rect, *args, **kwargs):
        x, y = self.translate(rect.x, rect.y)
        r = SDL_Rect(x, y, int(rect.w), int(rect.h))
        SDL_RenderCopy(self.renderer, texture, None, r)

    def draw_rect(self, rect, *args, **kwargs):
        x, y = self.translate(rect.x, rect.y)
        r = SDL_Rect(x, y, int(rect.w), int(rect.h))
        c = kwargs.pop('color', (255, 255, 255, 50))
        SDL_SetRenderDrawColor(self.renderer, *c)
        SDL_RenderDrawRect(self.renderer, r)

    def draw_line(self, x1, y1, x2, y2, *args, **kwargs):
        (x1, y1), (x2, y2) = self.translate(x1, y1), self.translate(x2, y2)
        c = kwargs.pop('color', (255, 255, 255, 50))
        SDL_SetRenderDrawColor(self.renderer, *c)
        SDL_RenderDrawLine(self.renderer, x1, y1, x2, y2)

    def draw_filled_rect(self, rect, *args, **kwargs):
        x, y = self.translate(rect.x, rect.y)
        r = SDL_Rect(x, y, int(rect.w), int(rect.h))
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
