from collections import deque

from ..math.vector import Vec
from .component import Component


class CanCollide(Component):
    pass


class AffectedByGravity(Component):
    pass


class Body(Component):

    def __init__(self, entity, *args, **kwargs):
        super().__init__(entity, *args, **kwargs)
        self.pos = Vec(kwargs.get('x', 0.0), kwargs.get('y', 0.0))
        self.vel = Vec(kwargs.get('vx', 0.0), kwargs.get('vy', 0.0))
        self.norm = Vec(kwargs.get('nx', 0.0), kwargs.get('ny', 0.0))
        self.acc = Vec(kwargs.get('ax', 0.0), kwargs.get('ay', 0.0))
        self.friction = Vec(kwargs.get('fx', 0.0), kwargs.get('fy', 0.0))
        self.w, self.h = kwargs.get('w', 10), kwargs.get('h', 10)
        self.mass = kwargs.get('mass', 1.0)
        self.colliding_with = []
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
