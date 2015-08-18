from . import system
from ..components.worldbound import WorldBound
from ..components.position import Position
from ..components.size import Size
from ..components.force import Force
from ..components.velocity import Velocity


class WorldBoundConstrainer(system.System):

    componenttypes = Force, Position, Size, Velocity, WorldBound

    def process(self, signaler, components):
        for f, p, s, v, wb in components:
            if p.x < 0:
                p.x = 0
                f.x = 0
                v.vx = 0
            if p.x + s.w > wb.maxx:
                p.x = wb.maxx - s.w
                f.x = 0
                v.vx = 0
            if p.y < 0:
                p.y = 0
                f.y = 0
                v.vy = 0
            if p.y + s.h > wb.maxy:
                p.y = wb.maxy - s.h
                f.y = 0
                v.vy = 0
