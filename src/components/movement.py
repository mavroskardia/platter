import math

from .component import Component
from ..math.vector import Vec, direction


class Shape(Component):

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
        return direction(self.vel)

    @property
    def moving(self):
        return abs(self.vel.x) > 0.1 or abs(self.vel.y) > 0.1
