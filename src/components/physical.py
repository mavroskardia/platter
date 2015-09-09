from collections import deque

from ..math.vector import Vec
from . import component


class CanCollide(component.Component):
    def __init__(self, entity, *args):
        super().__init__(entity, *args)
        self.colliding = False


class AffectedByGravity(component.Component):
    def __init__(self, entity, *args):
        super().__init__(entity, *args)
        self.affecting = True


class Body(component.Component):

    def __init__(self, *args, entity=None,
                 x=0, y=0, w=0, h=0,
                 vx=0, vy=0, ax=0, ay=0, nx=-1, ny=-1, mass=1.0, **kwargs):

        super().__init__(entity)
        self.pos = Vec(x, y)
        self.vel = Vec(vx, vy)
        self.norm = Vec(nx, ny)
        self.acc = Vec(ax, ay)
        self.w, self.h = w, h
        self.friction = Vec(0, 0)
        self.mass = mass
        self.colliding_on_x = False
        self.colliding_on_y = False

    def __str__(self):
        return '''Body for {s.entity.name}:
    Position:       {s.pos}
    Dimensions:     {s.w} x {s.h}
    Velocity:       {s.vel}
    Acceleration:   {s.acc}
'''.format(s=self)

    @property
    def falling(self):
        return self.vy > 0

    @property
    def jumping(self):
        return self.vy < 0
