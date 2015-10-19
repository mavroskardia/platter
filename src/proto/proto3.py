import sys
import os
import random

try:
    os.environ['PYSDL2_DLL_PATH'] = 'lib'
    from sdl2 import *
    from sdl2.sdlttf import *
except ImportError:
    print('Could not import SDL2')
    sys.exit(1)

from collections import defaultdict

from .. import config
from .. import signaler

from ..main.entity import Entity
from ..main.fps import Fps

from ..main.ecs import EntityComponentSystemManager
from ..math.vector import Vec
from ..systems.system import System
from ..systems.sdl import SdlSystem
from ..systems.input import InputSystem
from ..systems.decorations import VectorRendererSystem
from ..systems.sprite import SpriteSystem
from ..systems.map import MapSystem
from ..systems.movement import ShapeMovementSystem, ShapeRendererSystem
from ..components.component import Component
from ..components.decoration import Bordered
from ..components.movement import Shape
from ..components.sprite import Sprite


VectorRendererSystem.componenttypes = Shape,
SpriteSystem.componenttypes = Shape, Sprite


class WorldCollisionSystem(System):

    componenttypes = Shape,

    def process(self, *args, components, elapsed, **kwargs):

        for s, in components:
            if s.pos.x <= 0:
                s.pos.x = 1
            if s.pos.x >= config.resolution[0] - s.w:
                s.pos.x = config.resolution[0] - s.w - 1
            if s.pos.y <= 0:
                s.pos.y = 1
            if s.pos.y >= config.resolution[1] - s.h:
                s.pos.y = config.resolution[1] - s.h - 1
                s.jumping = False


class PlayerControlled(Component):
    pass


class PlayerInputSystem(System):

    componenttypes = PlayerControlled, Shape

    def process(self, *args, components, elapsed, **kwargs):
        kp = SDL_GetKeyboardState(None)

        for pc, shape in components:

            if kp[SDL_SCANCODE_LEFT]:
                shape.acc.x -= 1.0

            if kp[SDL_SCANCODE_RIGHT]:
                shape.acc.x += 1.0

            if kp[SDL_SCANCODE_SPACE]:
                if not shape.jumping:
                    shape.acc.y = -100.0
                    shape.jumping = True


def quit():
    sys.exit(0)


def proto():

    ecs = EntityComponentSystemManager()
    fps = Fps()

    fps.init()

    for sys in (SdlSystem, InputSystem, PlayerInputSystem,
                VectorRendererSystem, MapSystem, SpriteSystem,
                WorldCollisionSystem, ShapeMovementSystem,
                ShapeRendererSystem):
        ecs.add_system(sys(), init=True)

    signaler.instance.register('quit', quit)
    signaler.instance.register('keydown:Escape', quit)

    player = Entity('player')
    shape = Shape(player)
    shape.w = 37
    shape.h = 65
    player.components = [Bordered(player), PlayerControlled(player),
                         shape, Sprite(player, 'default')]

    ecs.add_entity(player)

    while True:
        ecs.process(fps.tick_start())
        fps.tick_end()

if __name__ == '__main__':

    proto()

    print('done')
