import sys
import os
import atexit
import time

try:
    os.environ['PYSDL2_DLL_PATH'] = 'lib'
    from sdl2 import *
    from sdl2.sdlttf import *
except ImportError:
    print('Could not import SDL2')
    sys.exit(1)

from collections import defaultdict

from .. import config
from ..main.signaler import Signaler


class Container:

    def __init__(self):
        self.components = defaultdict(list)

    def add(self, component):
        self.components[type(component)].append(component)


class RigidBody:

    def __init__(self, decorator):
        self.decorator = decorator


class Dynamic:
    pass


class Static:
    pass


class Renderable:

    def __init__(self, decorator):
        self.decorator = decorator

    def render(self, renderer):
        self.decorator.render(renderer)


class Bordered:

    def render(self, renderer):
        pass


def init_sdl():
    err = SDL_Init(SDL_INIT_EVERYTHING)
    if err != 0:
        raise Exception(SDL_GetError())

    window = SDL_CreateWindow(config.title.encode(), SDL_WINDOWPOS_CENTERED,
                              SDL_WINDOWPOS_CENTERED, config.resolution[0],
                              config.resolution[1], SDL_WINDOW_SHOWN)

    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)

    return renderer


def init_ttf():
    err = TTF_Init()
    if err != 0:
        raise Exception(TTF_GetError())

    font = TTF_OpenFont(config.hud_font.encode(), config.hud_font_size)
    if not font:
        raise Exception(TTF_GetError())

    return font


def update_physics(objects):
    pass


def render(renderer, alpha, objects):
    for obj in objects:
        for renderable in obj.components[Renderable]:
            renderable.render(renderer)


def add_dynamic_object(objects):

    dynobj = Container()
    dynobj.add(RigidBody(Dynamic()))
    dynobj.add(Renderable(Bordered()))

    objects.append(dynobj)


def add_static_object(objects):

    statobj = Container()
    statobj.add(RigidBody(Static()))
    statobj.add(Renderable(Bordered()))

    objects.append(statobj)


def proto():
    atexit.register(SDL_Quit)

    signaler = Signaler()
    renderer = init_sdl()
    font = init_ttf()

    evt = SDL_Event()
    last_time = time.time()
    accumulator = 0.0
    time_delta = 1 / 60

    objects = []

    running = True
    while running:
        current_time = time.time()
        accumulator += current_time - last_time
        last_time = current_time

        if accumulator > 0.2:
            accumulator = 0.2

        while accumulator > time_delta:
            update_physics(objects)
            accumulator -= time_delta

        alpha = accumulator / time_delta

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
        SDL_RenderClear(renderer)

        render(renderer, alpha, objects)

        SDL_RenderPresent(renderer)

        while SDL_PollEvent(evt):
            if evt.type == SDL_QUIT:
                running = False
            elif evt.type == SDL_KEYDOWN:
                if evt.key.keysym.scancode == SDL_SCANCODE_D:
                    add_dynamic_object(objects)
                elif evt.key.keysym.scancode == SDL_SCANCODE_S:
                    add_static_object(objects)
                elif evt.key.keysym.scancode == SDL_SCANCODE_ESCAPE:
                    running = False


if __name__ == '__main__':
    proto()
