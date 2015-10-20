from collections import namedtuple

from .system import System

from .. import signaler
from .. import config
from ..math.vector import Vec, direction
from ..components.movement import Shape
from ..components.decoration import Bordered


Rect = namedtuple('Rect', ['x', 'y', 'w', 'h'])


class ShapeRendererSystem(System):

    componenttypes = Bordered, Shape

    def process(self, *args, components, elapsed, **kwargs):
        for bordered, shape in components:
            signaler.instance.trigger('draw:rect', Rect(
                shape.pos.x, shape.pos.y, shape.w, shape.h))


class ShapeMovementSystem(System):

    componenttypes = Shape,

    def init(self):
        def setmap(map):
            self.map = map
        signaler.instance.trigger('get:map', setmap)

    def nocollision(self, newpos, shape):
        shape.pos = newpos
        # shape.jumping = True

    def collision(self, newpos, shape):
        if shape.vel.y > 0:
            shape.jumping = False

        dir = direction(newpos - shape.pos)

        if dir in ('left', 'right'):
            shape.pos.y = newpos.y
        elif dir in ('up', 'down'):
            shape.pos.x = newpos.x

    def process1(self, *args, components, elapsed, **kwargs):

        for s, in components:
            s.acc.y += 1.2  # gravity
            s.vel += s.acc
            nextpos = s.pos + s.vel * elapsed

            signaler.instance.trigger('handle_tile_collision',
                                      nextpos, s, self.nocollision,
                                      self.collision)

            # apply friction to everything
            s.acc *= 0.95
            s.vel *= 0.95

    def process(self, *args, components, elapsed, **kwargs):
        for s, in components:
            s.vel += s.acc
            nextpos = s.pos + s.vel * elapsed

            tx = nextpos.x // config.tile_width * 32
            ty = (nextpos.y + s.h) // config.tile_height * 32
            signaler.instance.trigger('draw:rect',
                                      Rect(tx, ty, 32, 32),
                                      color=(255, 0, 0, 255))

            d = direction(s.vel)

            if d == 'down':
                t = self.map.get_tile_at(nextpos.x + s.w/2, nextpos.y + s.h)
                if not t.can_walk:
                    nextpos.y = s.pos.y
                    s.vel.y = 0
                    s.jumping = False
            elif d == 'up':
                pass
            elif d == 'left':
                t = self.map.get_tile_at(nextpos.x, nextpos.y + s.h)
                if not t.can_walk:
                    nextpos.x = s.pos.x
            elif d == 'right':
                pass

            s.pos = nextpos

            # apply gravity
            s.acc.y += 1.2
            s.acc *= 0.95
            s.vel *= 0.95

    def resolve(self, tile, nextpos, shape):
        if tile.can_walk:
            shape.pos = nextpos
            return

        # the tile we are attempting to enter is unwalkable... back away,
        # but do so differently depending on entry...?

        dir = direction(nextpos - shape.pos)

        if dir == 'left':
            shape.pos.y = nextpos.y
        elif dir == 'right':
            shape.pos.y = nextpos.y
        elif dir == 'up':
            shape.pos.x = nextpos.x
        else:
            shape.pos.x = nextpos.x
