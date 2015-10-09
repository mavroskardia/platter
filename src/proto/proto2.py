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

from ..main.entity import Entity
from ..main.fps import Fps

from .. import config
from .. import signaler
from ..main.ecs import EntityComponentSystemManager
from ..math.vector import Vec
from ..systems.system import System
from ..systems.sdl import SdlSystem
from ..systems.input import InputSystem
from ..systems.physical import PhysicsSystem
from ..systems.decorations import BorderRendererSystem, VectorRendererSystem

from ..components.decoration import Bordered
from ..components.physical import HasPhysics, Body, CanCollide
from ..components.player import PlayerControl


class PlayerInputSystem(System):

    componenttypes = Body, PlayerControl

    def process(self, *args, components, elapsed, **kwargs):
        kp = SDL_GetKeyboardState(None)

        for body, pi in components:

            if kp[SDL_SCANCODE_LEFT]:
                body.vel.x -= 1.0

            if kp[SDL_SCANCODE_RIGHT]:
                body.vel.x += 1.0


def quit():
    sys.exit(0)


def add_entity(ecs):
    entity = Entity(random.random())
    entity.components.append(Body(entity, x=300, y=100, w=50, h=50, vx=0, vy=0,
                             mass=10.0))
    entity.components.append(Bordered(entity))
    entity.components.append(CanCollide(entity))
    entity.components.append(HasPhysics(entity))
    entity.components.append(PlayerControl(entity))
    ecs.add_entity(entity)


def add_platforms(ecs):
    entity = Entity(random.random())
    entity.components.append(Body(entity, x=0, y=config.resolution[1] - 50,
                                  w=config.resolution[0], h=50, mass=0))
    entity.components.append(Bordered(entity))
    entity.components.append(CanCollide(entity))
    entity.components.append(HasPhysics(entity, True))
    ecs.add_entity(entity)

    entity = Entity(random.random())
    entity.components.append(Body(entity, x=250, y=300, w=150, h=50, mass=0))
    entity.components.append(Bordered(entity))
    entity.components.append(CanCollide(entity))
    entity.components.append(HasPhysics(entity, True))
    ecs.add_entity(entity)


def proto():

    ecs = EntityComponentSystemManager()
    fps = Fps()

    fps.init()

    sdl = SdlSystem()
    sdl.init()

    ps = PhysicsSystem()
    ps.init()

    inps = InputSystem()
    inps.init()

    brs = BorderRendererSystem()
    brs.init()

    vrs = VectorRendererSystem()
    vrs.init()

    pinps = PlayerInputSystem()
    pinps.init()

    ecs.add_system(sdl)
    ecs.add_system(inps)
    ecs.add_system(ps)
    ecs.add_system(brs)
    ecs.add_system(vrs)
    ecs.add_system(pinps)

    add_platforms(ecs)

    signaler.instance.register('quit', quit)
    signaler.instance.register('keydown:A', lambda: add_entity(ecs))
    signaler.instance.register('keydown:Escape', quit)

    while True:
        ecs.process(fps.tick_start())
        fps.tick_end()

if __name__ == '__main__':

    proto()

    print('done')
