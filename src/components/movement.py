import math

from .component import Component
from ..math.vector import Vec


class Shape(Component):

    rot = math.cos(math.pi / 4)

    def __init__(self, entity):
        super().__init__(entity)
        self.pos = Vec(0, 0)
        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)
        self.w = 0
        self.h = 0
        self.jumping = True

    @property
    def direction(self):
        '''
            Returns one of 'left', 'right', 'down', or 'up'
        '''
        # we'll start by rotating the movement vector by π/4 so the rest is
        # easy peasy
        mv = self.vel
        rv = Vec(self.rot * mv.x + self.rot * mv.y,
                 -self.rot * mv.x + self.rot * mv.y)

        if rv.x >= 0 and rv.y >= 0:
            return 'down'
        if rv.x >= 0 and rv.y < 0:
            return 'right'
        if rv.x < 0 and rv.y >= 0:
            return 'left'
        if rv.x < 0 and rv.y < 0:
            return 'up'

    @property
    def moving(self):
        return abs(self.vel.x) > 0.1 or abs(self.vel.y) > 0.1
