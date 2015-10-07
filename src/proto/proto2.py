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
from ..systems.sdl import SdlSystem
from ..systems.input import InputSystem
from ..systems.physical import PhysicsSystem
from ..systems.decorations import BorderRendererSystem

from ..components.decoration import Bordered
from ..components.physical import HasPhysics, Body, CanCollide


def quit():
    sys.exit(0)


def add_entity(ecs):
    entity = Entity(random.random())
    entity.components.append(Body(entity,
                             x=random.randint(0, config.resolution[0]),
                             y=random.randint(0, config.resolution[1]),
                             w=random.randint(50, 300),
                             h=random.randint(50, 300),
                             vx=random.randint(-30, 30),
                             vy=random.randint(-30, 30),
                             mass=random.random() * 10.0))
    entity.components.append(Bordered(entity))
    entity.components.append(CanCollide(entity))
    entity.components.append(HasPhysics(entity))
    ecs.add_entity(entity)


def add_ground(ecs):
    entity = Entity(random.random())
    entity.components.append(Body(entity, x=0, y=config.resolution[1]-50,
                             w=config.resolution[0], h=50, mass=0))
    entity.components.append(Bordered(entity))
    entity.components.append(CanCollide(entity))
    entity.components.append(HasPhysics(entity))
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

    ecs.add_system(sdl)
    ecs.add_system(inps)
    ecs.add_system(ps)
    ecs.add_system(brs)

    add_ground(ecs)

    signaler.instance.register('quit', quit)
    signaler.instance.register('keydown:A', lambda: add_entity(ecs))
    signaler.instance.register('keydown:Escape', quit)

    while True:
        ecs.process(fps.tick_start())
        fps.tick_end()

if __name__ == '__main__':

    proto()

    print('done')
