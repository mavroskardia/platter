from . import system

from ..components.physical import Acceleration, Position, Velocity


class ForceSystem(system.System):

    componenttypes = Acceleration, Velocity

    def process(s, *args, signaler=None, components=None, elapsed=0, **kargs):
        for acc, vel in components:
            vel.vx += acc.x * elapsed
            vel.vy += acc.y * elapsed


class PositionUpdateSystem(system.System):

    componenttypes = Position, Velocity

    def process(s, *args, signaler=None, components=None, elapsed=0, **kargs):
        for pos, vel in components:
            pos.x += vel.vx * elapsed
            pos.y += vel.vy * elapsed
