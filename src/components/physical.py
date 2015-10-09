from copy import copy
from collections import deque, namedtuple

from ..math.vector import Vec
from .component import Component


class HasPhysics(Component):
    def __init__(self, entity, static=False, affected_by_gravity=True):
        super().__init__(entity)
        self.static = static
        self.affected_by_gravity = affected_by_gravity


class CanCollide(Component):
    pass


class Body(Component):

    Rect = namedtuple('Rect', ('x', 'y', 'w', 'h'))

    def __init__(self, entity, *args, **kwargs):
        super().__init__(entity, *args, **kwargs)

        # top-left position
        self.pos = Vec(kwargs.pop('x', 0.0), kwargs.pop('y', 0.0))
        # dimensions
        self.w, self.h = kwargs.pop('w', 10), kwargs.pop('h', 10)
        # velocity
        self.vel = Vec(kwargs.pop('vx', 0.0), kwargs.pop('vy', 0.0))

        # frictions
        self.static_friction = kwargs.pop('sf', 1.0)
        self.dynamic_friction = kwargs.pop('df', 0.3)

        # restitution
        self.restitution = kwargs.pop('r', 0.1)

        # inverse mass
        mass = kwargs.pop('mass', 1.0)
        self.im = 0 if mass == 0 else 1 / mass

        # calculation vars
        self.force = Vec(0, 0)
        self.update_bounds()

    def integrate_forces(self, f):
        if self.im != 0:
            self.vel += 0.5 * (self.force * self.im + f)

    def integrate_velocities(self, v):
        if self.im != 0:
            self.pos += self.vel
            self.integrate_forces(v)

    def apply_impulse(self, i):
        self.vel += self.im * i

    def apply_force(self, f):
        self.force += f

    def clear_forces(self):
        self.force = Vec(0, 0)

    def update_bounds(self):
        self.min = self.pos
        self.max = self.pos + Vec(self.w, self.h)

    def is_overlapping(self, other):
        return (self.pos.x < other.pos.x + other.w and
                self.pos.x + self.w > other.pos.x and
                self.pos.y < other.pos.y + other.h and
                self.pos.y + self.h > other.pos.y)

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
