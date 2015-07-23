from sdl2 import *


class SdlGraphics(object):

    def __init__(self, resolution=(1024, 768), *args, **kwargs):
        self.resolution = resolution
        self.title = kwargs.pop('title', 'Platter')
        self.window = None
        self.renderer = None

    def reset(self):
        if SDL_Init(SDL_INIT_VIDEO) != 0:
            return False, 'SDL_Init failed: {}'.format(SDL_GetError())

        self.window = SDL_CreateWindow(self.title.encode(),
                                       SDL_WINDOWPOS_CENTERED,
                                       SDL_WINDOWPOS_CENTERED,
                                       self.resolution[0],
                                       self.resolution[1],
                                       SDL_WINDOW_SHOWN)

        if not self.window:
            return False, 'SDL_CreateWindow failed: {}'.format(SDL_GetError())

        self.renderer = SDL_CreateRenderer(self.window, -1,
                                           SDL_RENDERER_ACCELERATED)

        if not self.renderer:
            return False,
            'SDL_CreateRenderer failed: {}'.format(SDL_GetError())

        self.clear()

        return True, None

    def clear(self):
        SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
        SDL_RenderClear(self.renderer)

    def render(self, state):
        self.clear()

        for actor in state.actors:
            actor.render(self.renderer)

        SDL_RenderPresent(self.renderer)

        SDL_Delay(16)
