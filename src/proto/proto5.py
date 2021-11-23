import sys

from dataclasses import dataclass

from src import signaler
from src.main.ecs import EntityComponentSystemManager
from src.main.fps import Fps
from src.systems.system import System
from src.systems.sdl import SdlSystem
from src.systems.input import InputSystem
from src.main.entity import Entity
from src.components.component import Component
from src.math.vector import Vec

@dataclass
class rect:
  x: int = 0
  y: int = 0
  w: int = 0
  h: int = 0


@dataclass
class Position(Component):
  vec: Vec = Vec(0, 0)


@dataclass
class Movement(Component):
  vec: Vec = Vec(0, 0)


@dataclass
class Shape(Component):
  w: int = 0
  h: int = 0


class ShapeRenderer(System):

  componenttypes = Position, Shape

  def process(self, *a, components=None, elapsed=0, **kw):
    for pos, shape in components:
      r = rect(int(pos.vec.x), int(pos.vec.y), shape.w, shape.h)
      signaler.instance.trigger('draw:filledrect', r, color=(255,255,0,255))


class MovementPositionVectorRenderSystem(System):

  componenttypes = Movement, Position, Shape

  threshold:float = 2.0
  exaggeration:float = 10.0

  def process(self, *a, components=None, elapsed=0, **kw):
    for mov, pos, shape in components:
      v1 = pos.vec + Vec(shape.w/2, shape.h/2)
      v2 = v1 + (mov.vec * self.exaggeration)

      # skip if too small
      if (v2-v1).length() < self.threshold:
        continue

      signaler.instance.trigger('draw:arrow', v1.x, v1.y, v2.x, v2.y,
        color=(255,0,0,255))


class ImpulseSystem(System):

  componenttypes = Movement, Position

  def process(self, *a, components=None, elapsed=0, **kw):
    for movement, pos in components:
      pos.vec += movement.vec


class FrictionSystem(System):

  componenttypes = Movement,

  def process(self, *a, components=None, elapsed=0, **kw):
    for movement in (c for c, in components):
      movement.vec *= 0.9


class InputHandlerSystem(System):

  componenttypes = Movement,

  def init(self):
    self.keysdown = {'Left': False, 'Right': False, 'Up': False, 'Down': False}
    signaler.instance.register('keydown:Right', self.handle_keydown('Right'))
    signaler.instance.register('keydown:Left', self.handle_keydown('Left'))
    signaler.instance.register('keydown:Up', self.handle_keydown('Up'))
    signaler.instance.register('keydown:Down', self.handle_keydown('Down'))
    signaler.instance.register('keyup:Right', self.handle_keyup('Right'))
    signaler.instance.register('keyup:Left', self.handle_keyup('Left'))
    signaler.instance.register('keyup:Up', self.handle_keyup('Up'))
    signaler.instance.register('keyup:Down', self.handle_keyup('Down'))

  def handle_keydown(self, which):
    def handle():
      self.keysdown[which] = True
    return handle

  def handle_keyup(self, which):
    def handle():
      self.keysdown[which] = False
    return handle

  def calc_impulse(self):
    x:float = 0.0
    y:float = 0.0

    if self.keysdown['Left']:
      x = -0.5
    if self.keysdown['Right']:
      x = 0.5
    if self.keysdown['Up']:
      y = -0.5
    if self.keysdown['Down']:
      y = 0.5

    return Vec(x, y)

  def process(self, *args, components=None, elapsed=0, **kwargs):
    impulse = self.calc_impulse()
    for movement in (c for c, in components):
      movement.vec += impulse


def proto():

  def quit():
    sys.exit(0)

  theshape = Entity('theshape', components=[
    Shape(10, 10),
    Position(Vec(10, 10)),
    Movement(),
  ])

  ecs = EntityComponentSystemManager()
  fps = Fps()
  fps.init()

  signaler.instance.register('quit', quit)

  ecs.add_system(SdlSystem(), init=True)
  ecs.add_system(InputSystem(), init=True)
  ecs.add_system(InputHandlerSystem(), init=True)
  ecs.add_system(ShapeRenderer())
  ecs.add_system(FrictionSystem())
  ecs.add_system(ImpulseSystem())
  ecs.add_system(MovementPositionVectorRenderSystem())


  ecs.add_entity(theshape)

  while True:
    ecs.process(fps.tick_start())
    fps.tick_end()


if __name__ == '__main__':
  proto()