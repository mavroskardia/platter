import sys
import os
import random
import ctypes

from math import factorial as fac

try:
    os.environ['PYSDL2_DLL_PATH'] = 'lib'
    from sdl2 import *
    from sdl2.sdlttf import *
except ImportError:
    print('Could not import SDL2')
    sys.exit(1)

from collections import defaultdict

from .. import signaler
from ..math.vector import Vec
from ..components.component import Component
from ..systems.system import System
from ..main.entity import Entity
from ..main.fps import Fps
from ..main.ecs import EntityComponentSystemManager


class SDLSystem(System):

    def init(self):
        SDL_Init(SDL_INIT_EVERYTHING)

        self.window = SDL_CreateWindow(b"Splines!",
                                       SDL_WINDOWPOS_CENTERED,
                                       SDL_WINDOWPOS_CENTERED,
                                       1000, 800,
                                       SDL_WINDOW_SHOWN)

        self.renderer = SDL_CreateRenderer(self.window, -1,
                                           SDL_RENDERER_ACCELERATED)

        signaler.instance.register('draw:path', self.draw_path)
        signaler.instance.register('draw:rects', self.draw_rects)

    def process(self, *args, components=None, elapsed=0, **kwargs):
        self.handle_inputs()
        self.render()

    def render(self):
        SDL_RenderPresent(self.renderer)
        SDL_SetRenderDrawColor(self.renderer, 0,0,0,0)
        SDL_RenderClear(self.renderer)
        SDL_Delay(17)

    def handle_inputs(self):

        event = SDL_Event()

        while SDL_PollEvent(event):

            if event.type == SDL_QUIT:
                signaler.instance.trigger('quit')

            elif event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_ESCAPE:
                    signaler.instance.trigger('quit')

            elif event.type == SDL_MOUSEBUTTONDOWN and signaler.instance.has_handler_for_event('mouse:down'):
                signaler.instance.trigger('mouse:down', Vec(event.button.x,event.button.y))

            elif event.type == SDL_MOUSEBUTTONUP and signaler.instance.has_handler_for_event('mouse:up'):
                signaler.instance.trigger('mouse:up', Vec(event.button.x,event.button.y))

            elif event.type == SDL_MOUSEMOTION and signaler.instance.has_handler_for_event('mouse:move'):
                signaler.instance.trigger('mouse:move', Vec(event.motion.x, event.motion.y))


    def draw_path(self, points, *args, **kwargs):
        point_count = len(points)
        point_array = ctypes.pointer((SDL_Point * point_count)())

        for i in range(point_count):
            point_array.contents[i] = SDL_Point(int(points[i].x), int(points[i].y))

        SDL_SetRenderDrawColor(self.renderer, 200, 0, 0, 255)
        SDL_RenderDrawLines(self.renderer, point_array.contents[0], point_count)

    def draw_rects(self, rects, width, height, *args, **kwargs):
        rect_count = len(rects)
        rect_array = ctypes.pointer((SDL_Rect * rect_count)())

        for i in range(rect_count):
            rect_array.contents[i] = SDL_Rect(int(rects[i].x), int(rects[i].y), width, height)

        SDL_SetRenderDrawColor(self.renderer, 0, 0, 200, 255)
        SDL_RenderDrawRects(self.renderer, rect_array.contents[0], rect_count)


class ControlPoint(Component):

    def __init__(self, entity, vec2, *args, **kwargs):
        super().__init__(entity, *args, **kwargs)
        self.vec = vec2


class Bezier(System):

    componenttypes = ControlPoint,

    sample_rate = 100  # number of steps from 0 to 1 for the curve

    def init(self):
        signaler.instance.register('mouse:down', self.handle_mousedown)
        signaler.instance.register('mouse:up', self.handle_mouseup)
        self.grabbed_cp = None

    def calc(self, cps):
        '''
            Generalized Bezier formula is:
            B(t) = Sum(i->n: binco(n,i)*(1-t)^(n-i)*t^i*Pi)
        '''

        t = 0
        n = len(cps) - 1
        points = []

        while t <= 1:
            v = Vec(0,0)
            for i in range(len(cps)):
                v += fac(n) / (fac(i) * fac(n - i)) * t**i * (1 - t)**(n - i) * cps[i]
            points.append(v)
            t += 1 / self.sample_rate

        return points

    def process(self, *args, components=None, elapsed=0, **kwargs):
        self.cps = tuple(c.vec for c, in components)
        signaler.instance.trigger('draw:path', self.calc(self.cps))
        signaler.instance.trigger('draw:rects', self.cps, 10, 10)

    def handle_mousedown(self, point, *args, **kwargs):
        self.grabbed_cp = self.cp_at(point)
        if self.grabbed_cp:
            signaler.instance.register('mouse:move', self.handle_mousemove)
        else:
            e = Entity('cp{},{}'.format(point.x,point.y))
            e.components.append(ControlPoint(e, point))
            signaler.instance.trigger('add_entity', e)

    def handle_mouseup(self, *args, **kwargs):
        self.grabbed_cp = None
        signaler.instance.unregister('mouse:move', self.handle_mousemove)

    def handle_mousemove(self, point, *args, **kwargs):
        self.grabbed_cp.x = point.x
        self.grabbed_cp.y = point.y

    def cp_at(self, point):
        for cp in self.cps:
            if point.overlaps(cp, 20):
                return cp
        return None


def quit():
    sys.exit(0)

def proto():

    ecs = EntityComponentSystemManager()
    fps = Fps()

    fps.init()

    basename = 'thecurve'
    for i in range(4):
        name = '{}{}'.format(basename, i)
        entity = Entity(name)
        x = random.randint(100, 900)
        y = random.randint(100, 700)
        cp = ControlPoint(entity, Vec(x, y))
        entity.components.append(cp)
        ecs.add_entity(entity)

    signaler.instance.register('quit', quit)
    signaler.instance.register('keydown:Escape', quit)

    ecs.add_system(SDLSystem(), True)
    ecs.add_system(Bezier(), True)

    while True:
        ecs.process(fps.tick_start())
        fps.tick_end()

if __name__ == '__main__':
    proto()
    print('done')
