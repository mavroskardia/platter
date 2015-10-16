from collections import namedtuple

from .system import System

from .. import signaler
from ..components.movement import Shape
from ..components.decoration import Bordered


class ShapeRendererSystem(System):

    componenttypes = Bordered, Shape

    Rect = namedtuple('Rect', ['x', 'y', 'w', 'h'])

    def process(self, *args, components, elapsed, **kwargs):
        for bordered, shape in components:
            signaler.instance.trigger('draw:rect', self.Rect(
                shape.pos.x, shape.pos.y, shape.w, shape.h))


class ShapeMovementSystem(System):

    componenttypes = Shape,

    def setpos(self, newpos, shape):
        shape.pos = newpos

    def process(self, *args, components, elapsed, **kwargs):

        for s, in components:
            s.vel += s.acc
            nextpos = s.pos + s.vel * elapsed

            signaler.instance.trigger('no_tile_collision', nextpos, s)

            s.pos = nextpos

            # apply friction to everything
            s.acc *= 0.95
            s.vel *= 0.95

            if s.jumping:
                s.acc.y += 1.2
