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

from ..systems.sdl import SdlSystem
from ..systems.input import InputSystem
from ..systems.physical import PhysicsSystem

from ..components.physical import HasPhysics, Body, CanCollide


def quit():
    sys.exit(0)


def add_entity(ecs):
    entity = Entity(random.random())
    entity.components.append(Body(entity))
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

    ecs.add_system(sdl)
    ecs.add_system(inps)
    ecs.add_system(ps)

    signaler.instance.register('quit', quit)
    signaler.instance.register('keydown:A', lambda: add_entity(ecs))

    while True:
        ecs.process(fps.tick_start())
        fps.tick_end()

if __name__ == '__main__':

    proto()

    print('done')
