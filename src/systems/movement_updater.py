from . import system

from ..components.position import Position
from ..components.velocity import Velocity


class MovementUpdater(system.System):

    componenttypes = Position, Velocity

    def process(self, signaler, components):
        for p, v in components:
            p.x += v.vx
            p.y += v.vy
