from collections import namedtuple

from .system import System

from .. import signaler
from ..math.vector import Vec
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

    def nocollision(self, newpos, shape):
        shape.pos = newpos
        # shape.jumping = True

    def collision(self, newpos, shape):
        if shape.vel.y > 0:
            shape.jumping = False

    def process(self, *args, components, elapsed, **kwargs):

        for s, in components:
            s.vel += s.acc
            nextpos = s.pos + s.vel * elapsed

            signaler.instance.trigger('handle_tile_collision',
                                      nextpos, s, self.nocollision,
                                      self.collision)

            # apply friction to everything
            s.acc *= 0.95
            s.vel *= 0.95

            if s.jumping:
                s.acc.y += 1.2

    def resolve(self, tile, nextpos, shape, dt):
        if tile.can_walk:
            shape.pos = nextpos
            return

        # the tile we are attempting to enter is unwalkable... back away,
        # but do so differently depending on entry...?

        dir = direction(nextpos - shape.pos)

        if dir == 'left':

            pass
        elif dir == 'right':
            pass
        elif dir == 'up':
            pass
        else:
            pass

        pen = nextpos - shape.pos
        shape.pos -= pen
