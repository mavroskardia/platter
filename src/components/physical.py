from collections import deque

from . import component


class Jumping(component.Component):
    def __init__(self, entity, *args):
        super().__init__(entity, *args)
        self.in_progress = False


class CanCollide(component.Component):
    def __init__(self, entity, *args):
        super().__init__(entity, *args)
        self.colliding = False


class AffectedByGravity(component.Component):
    def __init__(self, entity, *args):
        super().__init__(entity, *args)
        self.affecting = True


class Acceleration(component.Component):
    def __init__(self, entity, xacc=0.0, yacc=0.0, *args):
        super().__init__(entity, *args)
        self.x = xacc
        self.y = yacc


class Position(component.Component):
    def __init__(self, entity, x=0, y=0, *args):
        super().__init__(entity)
        self.prevx = deque()
        self.prevy = deque()
        self.x = x
        self.y = y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)


class Size(component.Component):

    def __init__(self, entity, width=0, height=0, *args):
        super().__init__(entity, *args)
        self.w = width
        self.h = height

    def __repr__(self):
        return '{}x{}'.format(self.w, self.h)


class Velocity(component.Component):

    def __init__(self, entity, vx=0.0, vy=0.0, *args):
        super().__init__(entity)
        self.vx = vx
        self.vy = vy

    @property
    def falling(self):
        return self.vy > 0

    @property
    def jumping(self):
        return self.vy < 0
