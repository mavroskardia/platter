from collections import namedtuple


class Velocity(object):

    def __init__(self, vx=0.0, vy=0.0):
        self.vx = vx
        self.vy = vy

        self.directions = {'up': False, 'down': False,
                           'left': False, 'right': False}
