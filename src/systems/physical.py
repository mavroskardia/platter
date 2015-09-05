from . import system

from ..components.physical import Acceleration, Position, Velocity


class ForceSystem(system.System):

    componenttypes = Acceleration, Velocity

    def process(self, *args, signaler=None, entities=None, elapsed=0, **kargs):
        for acc, vel in entities:
            vel.vx += acc.x * elapsed
            vel.vy += acc.y * elapsed


class PositionUpdateSystem(system.System):

    componenttypes = Position, Velocity

    def process(self, *args, signaler=None, entities=None, elapsed=0, **kargs):
        for pos, vel in entities:
            pos.x += vel.vx * elapsed
            pos.y += vel.vy * elapsed
