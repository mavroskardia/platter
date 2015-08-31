from collections import deque


class AffectedByGravity:
    pass


class Acceleration:
    def __init__(self, xacc=0.0, yacc=0.0):
        self.x = xacc
        self.y = yacc


class Position(object):
    def __init__(self, x=0, y=0):
        self.prevx = deque()
        self.prevy = deque()
        self.x = x
        self.y = y
        self.nextx = 0
        self.nexty = 0

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)


class Size(object):

    def __init__(self, width=0, height=0):
        self.w = width
        self.h = height

    def __repr__(self):
        return '{}x{}'.format(self.w, self.h)


class Velocity(object):

    def __init__(self, vx=0.0, vy=0.0):
        self.vx = vx
        self.vy = vy
