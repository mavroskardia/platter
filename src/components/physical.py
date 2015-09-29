from copy import copy
from collections import deque, namedtuple

from ..math.vector import Vec
from .component import Component


class CanCollide(Component):
    pass


class AffectedByGravity(Component):
    pass


class Body(Component):

    Rect = namedtuple('Rect', ('x', 'y', 'w', 'h'))

    class MinMax:
        def __init__(self, x1, y1, x2, y2):
            self.min = Vec(x1, y1)
            self.max = Vec(x2, y2)

    def __copy__(self):
        b = Body
        b.pos = copy(self.pos)
        b.vel = copy(self.vel)
        b.norm = copy(self.norm)
        b.acc = copy(self.acc)
        b.friction = copy(self.friction)
        b.restitution = copy(self.restitution)
        b.w = copy(self.w)
        b.h = copy(self.h)
        b.mass = copy(self.mass)
        b.inv_mass = copy(self.inv_mass)
        return b

    def __init__(self, entity, *args, **kwargs):
        super().__init__(entity, *args, **kwargs)
        self.pos = Vec(kwargs.get('x', 0.0), kwargs.get('y', 0.0))
        self.vel = Vec(kwargs.get('vx', 0.0), kwargs.get('vy', 0.0))
        self.norm = Vec(kwargs.get('nx', 0.0), kwargs.get('ny', 0.0))
        self.acc = Vec(kwargs.get('ax', 0.0), kwargs.get('ay', 0.0))
        self.friction = Vec(kwargs.get('fx', 0.0), kwargs.get('fy', 0.0))
        self.restitution = kwargs.get('r', 10.0)
        self.w, self.h = kwargs.get('w', 10), kwargs.get('h', 10)
        self.mass = kwargs.get('mass', 1.0)
        self.inv_mass = 0 if self.mass == 0 else 1 / self.mass
        self.colliding_with = set()
        self.jumping = False

    def __str__(self):
        return '''Body for {s.entity.name}:
    Position:       {s.pos}
    Dimensions:     {s.w} x {s.h}
    Velocity:       {s.vel}
    Acceleration:   {s.acc}
'''.format(s=self)

    @property
    def moving(self):
        return self.vel.x > 0 or self.vel.y > 0

    def higher_than(self, other):
        return self.pos.y + self.h >= other.pos.y

    @property
    def direction(self):
        if self.vel.y < 0:
            return 'up'
        elif self.vel.y > 0:
            return 'down'
        elif self.vel.x > 0:
            return 'right'
        else:
            return 'left'

    def as_rect(self):
        return Body.Rect(self.pos.x, self.pos.y, self.w, self.h)

    def as_minmax(self):
        return Body.MinMax(self.pos.x, self.pos.y,
                           self.pos.x + self.w, self.pos.y + self.h)
