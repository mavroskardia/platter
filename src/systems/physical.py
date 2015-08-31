from . import system

from ..components.physical import Acceleration, Position, Velocity


class ForceSystem(system.System):

    componenttypes = Acceleration, Velocity

    def process(self, *args, signaler=None, entities=None, elapsed=0, **kargs):
        for e in entities:
            acc, vel = e.components
            vel.x += acc.x * elapsed
            vel.y += acc.y * elapsed


class PositionUpdateSystem(system.System):

    componenttypes = Position, Velocity

    def process(self, *args, signaler=None, entities=None, elapsed=0, **kargs):
        for e in entities:
            pos, vel = e.components
            pos.x += vel.x * elapsed
            pos.y += vel.y * elapsed
